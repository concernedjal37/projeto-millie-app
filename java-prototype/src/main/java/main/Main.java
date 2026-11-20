package main;

import java.io.IOException;
import java.time.Duration;
import java.util.ArrayList;
import java.util.List;

import io.github.cdimascio.dotenv.Dotenv;

import java.util.Scanner;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;

import main.dto.GeckoItineraries;
import main.dto.GeckoOffers;
import main.dto.Gecko_Request;
import main.dto.Gecko_Response;
import main.dto.Transferencia_Boni;
import main.dto.Compra_Boni;
import main.dto.Adesao_Boni;
import main.service.GeckoAPI;
import main.dto.Cotacao;

public class Main {
    private static final String HOST_TAILSCALE = "100.79.171.116"; 
    private static final String PORTA = "3306";
    private static final String BANCO = "Banco_da_Millie";
    private static final Object lock = new Object();
    
    public static void main(String[] args) throws IOException, InterruptedException {
        System.out.println("Iniciando programa");
        // 1. THREAD de Trabalho (contínuo)
        Thread workerThread = new Thread(() -> {
            // Iteração contínua para aguardar start (standby) e execução do trabalho
            while(true){
                // Script de aguarde de gatilho -> "Start"
                synchronized (lock) {
                    try {
                        System.out.println("[worker] em stand by. aguardando start...");
                        lock.wait(); // Execução pause até receber start
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                        break;
                    }     
                }
                // Script contínuo do código a ser executado
                //Extração de dados do GeckoAPI "passagens aéreas"
                Gecko_Response responseDTO = scrapingData();

                if (responseDTO == null || responseDTO.getData() == null || responseDTO.getData().getItineraries() == null) {
                    System.err.println("[ERRO] Aguardando novo comando...");
                    continue; // Volta para o início do loop e aguarda novo start
                }
                
                // Lista os resultados encontrados
                listItineraries(responseDTO.getData().getItineraries());
                // Identifica o itinerário de menor preço em dinheiro
                GeckoItineraries itinerary_menor_preco = encontraMenor(responseDTO.getData().getItineraries());
                // extraindo valor do itinerario mais barato
                double precoDinheiro = itinerary_menor_preco.getCheapestOffer().getTotal().getAmount();
                String moeda = itinerary_menor_preco.getCheapestOffer().getTotal().getCurrency();

                System.out.println("=".repeat(40) + "\nViagem mais econômica (Dinheiro)");
                System.out.println("Origem: " + itinerary_menor_preco.getOrigin());
                System.out.println("Destino: " + itinerary_menor_preco.getDestination());
                System.out.println("Duração: " + formatDuration(itinerary_menor_preco.getDuration()));
                System.out.println("Número de paradas: " + itinerary_menor_preco.getStopCount());
                System.out.println("Valor: " + moeda + " " + String.format("%.2f", precoDinheiro));

                // ====================================================================
                // CÁLCULO E COMPARAÇÃO DE MODALIDADES DE PAGAMENTO
                // ====================================================================
                // Estabelecendo valor da passagem mais barata
                double preco_passagem_barata = itinerary_menor_preco.getCheapestOffer().getTotal().getAmount();
                // Instanciando as listas de promoções no banco de dados
                List<Transferencia_Boni> lista_transferencias = new ArrayList<>();
                List<Compra_Boni> lista_compras = new ArrayList<>();
                List<Adesao_Boni> lista_adesao = new ArrayList<>();
                // função de busca das promoções no banco de dados
                extrairPromo_BD(lista_transferencias, lista_compras, lista_adesao);

                // função de extrair tabela com os valores de cotação de cada agencia de milhas
                List<Cotacao> lista_cotacoes = extrairCota_BD();

                System.out.println("[SISTEMA] Imprimindo todas as listas extraidas do banco de dados");
                // Impressão das listas extraidas
                // Imprimindo Lista de Transferencia Bonificada
                if(!lista_transferencias.isEmpty()){
                    System.out.println("Tabela Transferencia Bonificada");
                    System.out.println("  id  |  Origem  |  Destino  |  Valor Mínimo  |  Valor Máximo  |");
                    for(Transferencia_Boni transferencia: lista_transferencias){
                        transferencia.printTransf();
                    }
                }else{System.out.println("Lista de transferencia bonificada vazia");}

                // Imprimindo Lista de Compra Bonificada
                if(!lista_compras.isEmpty()){
                    System.out.println("Tabela Compra Bonificada");
                    System.out.println("  id  |  Origem   |  Valor Mínimo  |  Valor Máximo  |");
                    for(Compra_Boni compra: lista_compras){
                        compra.printCompra();
                    }
                }else{System.out.println("Lista de compra bonificada vazia");}

                // Imprimindo Lista de Adesão Bonificada
                if(!lista_adesao.isEmpty()){
                    System.out.println("Tabela Adesao Bonificada");
                    System.out.println("  id  |  Origem  |  Destino  |  Valor Mínimo  |  Valor Máximo  |");
                    for(Adesao_Boni Adesao: lista_adesao){
                        Adesao.printAdesao();
                    }
                }else{System.out.println("Lista de adesao bonificada vazia");}

                // Imprimindo Lista de Cotações
                if(!lista_cotacoes.isEmpty()){
                    System.out.println("Tabela Cotacoes");
                    System.out.println("  id  |  Origem  |  Destino  |  Valor Mínimo  |  Valor Máximo  |");
                    for(Cotacao cota: lista_cotacoes){
                        cota.printCota();
                    }
                }else{System.out.println("Lista de cotacoes vazia");}


                System.out.println("[SISTEMA] Promoções e cotações extraidas com sucesso");

                //=============================================================================================================
                // Dados da passagem em milhas (simulação) *tal valor vem direto da pesquisa da gecko no site da smiles ou azul 
                double preco_passagem_milhas = 40000.0;
                //=============================================================================================================
                //Calculando valores chave
                // 1º Valor por milheiro na agencia de origem (transferencia bonificada)
                double valor_milheiro_transf = 0.0;
                if(!lista_transferencias.isEmpty()){
                    int conta_promo = 0;
                    Transferencia_Boni maior_transf = lista_transferencias.get(0);
                    for(Transferencia_Boni transferencia:lista_transferencias){
                        if(transferencia.getDestino().equalsIgnoreCase("AZUL")){
                            maior_transf = transferencia;
                            conta_promo++;
                        }
                    } // selecionando somente valor da Azul para iniciar verificação
                    if(conta_promo>0){
                        for(Transferencia_Boni transferencia : lista_transferencias){
                            if(transferencia.getDestino().equalsIgnoreCase("AZUL")&&
                                (transferencia.getPercentMax()>maior_transf.getPercentMax())){
                                    maior_transf = transferencia;
                            }
                        }
                        // Cálculo do valor do milheiro por meio da promoção
                        valor_milheiro_transf = maior_transf.getValorMilhasOrigem()/(1+(maior_transf.getPercentMax()/100.0));

                        maior_transf.printTransf();
                        // Aprimorar para enviar dados ao flutter (identificando melhor opção)
                        boolean opcao_transf = avaliarOpcao(
                            "Transferência de pontos",
                            preco_passagem_barata,
                            preco_passagem_milhas,
                            valor_milheiro_transf
                        );

                    }else{System.out.println("Não existe transferencias bonificadas para AZUL");}   
                }else{System.out.println("Não existe promoções de transferencia bonificada");}
                
                // 2º passo Valor por milheiro da compra bonificada
                double valor_milheiro_compra = 0.0;
                if(!lista_compras.isEmpty()){
                    int conta_promo = 0;
                    Compra_Boni maior_compra = lista_compras.get(0);
                    for(Compra_Boni compra: lista_compras){
                        if(compra.getOrigem().equalsIgnoreCase("AZUL"))
                            maior_compra = compra;
                            conta_promo++;
                    }// selecionar compras da azul
                    if(conta_promo >0){
                        for(Compra_Boni compra : lista_compras){
                            if(compra.getOrigem().equalsIgnoreCase("AZUL") && 
                                (compra.getPercentMax()>maior_compra.getPercentMax())){
                                    maior_compra = compra;      
                            }
                        }
                        // Cálculo do valor do milheiro por meio da promoção
                        valor_milheiro_compra = maior_compra.getValorMilhasOrigem()/(1+(maior_compra.getPercentMax()/100.0));

                        // Comparativo: Compra Bonificada
                        // Aprimorar para enviar dados ao flutter (identificando melhor opção)
                        maior_compra.printCompra();
                        boolean opcao_compra =avaliarOpcao(
                            "Compra bonificada de pontos",
                            preco_passagem_barata,
                            preco_passagem_milhas,
                            valor_milheiro_compra
                        );
                    }else{System.out.println("Não existe compra bonificada para AZUL");}
                }else{System.out.println("Não existe promoções de compra bonificada");}
                
                // Avaliando cotação
                Cotacao cota_azul = new Cotacao();
                if(!lista_cotacoes.isEmpty()){
                    int conta_cota = 0;
                    for(Cotacao cota: lista_cotacoes){
                        if(cota.getAgencia().equalsIgnoreCase("AZUL")){
                            cota_azul = cota;
                            conta_cota++;
                        }
                    }// selecionando dentro da lista apenas as cotações da azul
                    // Extração de cotação de milhas da companhia operadora da viagem
                    if(conta_cota>0){
                        for (Cotacao cota: lista_cotacoes) {
                            if(cota.getAgencia().equalsIgnoreCase("AZUL") && cota.getValorMin()<cota_azul.getValorMin()){
                                cota_azul = cota;
                            }
                        }
                        // Comparando com contacoes
                        // Aprimorar para enviar dados ao flutter (identificando melhor opção)
                        cota_azul.printCota();
                        boolean opcao_cota = avaliarOpcao(
                            "Compra via cotação",
                            preco_passagem_barata,
                            preco_passagem_milhas,
                            cota_azul.getValorMax()
                        );
                    }else{System.out.println("Não existe cotação para AZUL");}
                }else{System.out.println("Não existe lista de cotações no banco de dados.");}
                
                
        }
    });
    workerThread.start();

    // 2. THREAD de Controle (gatilho Start / Finish)
    Scanner scanner = new Scanner(System.in);
    System.out.println("Digite 'start' para iniciar / 'finish' para encerrar");

    while (true) {
        String comando = scanner.nextLine();
        if (comando.equalsIgnoreCase("start")) {
            disparaStart();
        } else if (comando.equalsIgnoreCase("finish")) {
            System.err.println("Encerrando sistema...");
            scanner.close();
            System.exit(0);
        }
    }
}

    public static void disparaStart(){
        synchronized (lock) {
            System.out.println("[Gatilho] sinal de start enviado");
            lock.notify();
        }
    }
    public static Gecko_Response scrapingData(){
        System.out.println("Estabelecendo Objeto de Request");
        // Intanciando Objetos de Request
        GeckoAPI geckoAPI = new GeckoAPI();
        Gecko_Request requestDto = new Gecko_Request();
        // Set Valores para Objetos Request
        setRequest(geckoAPI, requestDto);
        // Extraindo chave Gecko API da variável de ambiente
        Dotenv dotenv = Dotenv.load();
        String myApiKey = dotenv.get("GECKO_API_KEY");
        // Chave Gecko API para teste inicial simples desconsiderar após extração da variável de ambiente funcionar
        // Enviando Request para Gecko API
        System.out.println("Iniciando scraping...");
        Gecko_Response response = geckoAPI.extrairDados(myApiKey, requestDto); // Função de scrapping de dados API
        if (response == null || response.getData() == null || response.getData().getItineraries() == null) {
            System.err.println("[ERRO] Falha ao obter itinerários da API Gecko\n" + "=".repeat(40));
            return null; // Volta para o início do loop e aguarda novo start
        }
        // Imprimindo Resposta "Response" recebida do scraping de dados
        System.out.println("Request ID: " + response.getRequestId());
        System.out.println("Execution Time: " + response.getexecutionId());
        System.out.println("Not Found: " + response.getNotFound());
        System.out.println("Link: " + response.getData().getUrl());

        // Condicionamento para manipulação de dados
        if (Boolean.TRUE.equals(response.getNotFound())){ // Responsta não encontrou dados para os parâmetros de request
            System.out.println("[AVISO]Nenhum resultado encontrado para a pesquisa.");
            return response;

        }else if(response.getData() != null) {// Resposta com dados encontrados
            System.out.println("[SISTEMA] Dados extraídos com sucesso:");
            System.out.println("Fonte de Pesquisa: " + response.getData().getSource());
            System.out.println("Tipo de Pesquisa: " + response.getData().getSearchType() + "*=*".repeat(50));
            return response;

        }else{ // Resposta não apresentou dado algum (provável erro no scrapping)
            System.out.println("[ERRO] A resposta veio sem dados." + "*=*".repeat(50));
            return response;
        }
    }
    public static void setRequest(GeckoAPI geckoAPI, Gecko_Request requestDto){
        System.out.println("Estabelecendo Objeto de Request");
        System.out.println("""
                               Set Valores de Objeto Request
                               """ + "=".repeat(40));
            requestDto.setTarget("voegol.com.br");
            requestDto.setType("plp");
            requestDto.setFrom("CNF");
            requestDto.setTo("AJU");
            requestDto.setDepartureDate("2026-12-23");
            requestDto.setReturnDate("2026-12-30");
            requestDto.setNumAdults(1);
            requestDto.setNumChildren(0);
            requestDto.setNumInfants(0);
        

    }
    public static void listItineraries(List<GeckoItineraries> itineraries){
        if(itineraries != null){
            for(GeckoItineraries itinerary : itineraries){
                System.out.println("=".repeat(40));
                System.out.println("Companhia aérea GOL");
                System.out.println("Origem: " + itinerary.getOrigin());
                System.out.println("Destino: " + itinerary.getDestination());
                System.out.println("Duração: " + formatDuration(itinerary.getDuration()));

                for(GeckoOffers offer: itinerary.getGeckoOffers()){
                    System.out.print("Tipo de Tarifa: ");
                    switch (offer.getBrandId()) {
                        case "LI":
                            System.out.println("Light");
                            break;
                        case "CL":
                            System.out.println("Classic");
                            break;
                        case "FL":
                            System.out.println("Flex");
                            break;
                        default:
                            System.err.println("N/A");
                            break;
                    }
                    System.out.println("Moeda: " + offer.getTotal().getCurrency());
                    System.out.println("Preço: " + offer.getTotal().getAmount());
                    System.out.println("=".repeat(40));
                }
            }
        }

    }
    public static String formatDuration(String isoDuration){
        Duration duration = Duration.parse(isoDuration);
        Long hours = duration.toHours();
        Long minutes = duration.toMinutes() %60;

        return hours + " H " + minutes + " Min";
    }
    public static GeckoItineraries encontraMenor(List<GeckoItineraries> itineraries){
        GeckoItineraries itineraryBarato = null;
        double menorPreco = Double.MAX_VALUE;

        if(itineraries != null){
            for(GeckoItineraries itinerary : itineraries){
                double preco = itinerary.getCheapestOffer().getTotal().getAmount();
                if(preco < menorPreco){
                    menorPreco = preco;
                    itineraryBarato = itinerary;
                }
            }
            if(itineraryBarato != null){
                return  itineraryBarato;
            }
        }
        return null;
    }
    public static void extrairPromo_BD(List<Transferencia_Boni> transferencias, List<Compra_Boni> compras, List<Adesao_Boni> adesoes){
        
        System.out.println("[SISTEMA] extraindo dados credenciais de acesso ao Banco de dados");
        // Extraindo variaveis de ambiente
        Dotenv dotenv = Dotenv.load();
        String USUARIO = dotenv.get("USER");
        String SENHA = dotenv.get("PASSWORD");

        System.out.println("[SISTEMA] construindo ponto de acesso...");
        // criando url de conexão ao Banco_da_Millie por meio do app Tailscale;
        String url = "jdbc:mariadb://100.79.171.116:3306/Banco_da_Millie?user=java_user&password=50BMG";
       
        System.out.println("[SISTEMA] extraindo dados de promoção no banco de dados Millie, promoções...");
        // Extraindo dados da tabela de promoções de transferência bonificada do banco de dados
        String sql ="""
            select * from Verificar_Transferencia_Boni;
        """;

        System.out.println("[SISTEMA] extraindo dados de transferencias bonificadas");
        try (Connection conection = DriverManager.getConnection(url);
            PreparedStatement stmt = conection.prepareStatement(sql);
            ResultSet resultado = stmt.executeQuery()){
                while (resultado.next()) {
                    // Lê linha por linha até não haver mais linhas para ler
                    int id = resultado.getInt("id");
                    String link = resultado.getString("link");
                    String origem = resultado.getString("plataforma_de_origem");
                    String data_vencimento = resultado.getString("data_limite");
                    double valor_milheiro_origem = resultado.getDouble("valor_milheiro_origem");
                    String destino = resultado.getString("plataforma_de_destino");
                    double percent_max = resultado.getDouble("percentual_MAX");
                    double percent_min = resultado.getDouble("percentual_MIN");
                    // cria o objeto dos dados extraidos para adicionar a lista
                    Transferencia_Boni obj = new Transferencia_Boni(id,link,origem,destino,percent_min,percent_max,valor_milheiro_origem,data_vencimento);
                    transferencias.add(obj);
                }
            System.out.println("[SISTEMA] Extração completa [1/3] \n" + "=".repeat(50));

            } catch (Exception e) {
            System.out.println("Erro ao extrair dados de transferência bonificada!! \n[ERRO] " + e);
            }

        sql = """
            select * from Verificar_Compra_Boni;
        """;
        System.out.println("[SISTEMA] extraindo dados de compras bonificadas");
        try (Connection conection = DriverManager.getConnection(url);
            PreparedStatement stmt = conection.prepareStatement(sql);
            ResultSet resultado = stmt.executeQuery()){
                while (resultado.next()) {
                    // Lê linha por linha até não haver mais linhas para ler
                    int id = resultado.getInt("id");
                    String link = resultado.getString("link");
                    String origem = resultado.getString("plataforma_de_origem");
                    String data_vencimento = resultado.getString("data_limite");
                    double valor_milheiro_agencia = resultado.getDouble("valor_milheiro_agencia");
                    double percent_max = resultado.getDouble("percentual_MAX");
                    double percent_min = resultado.getDouble("percentual_MIN");
                    // cria o objeto dos dados extraidos para adicionar a lista
                    Compra_Boni obj = new Compra_Boni(id,link, origem, percent_min, percent_max, valor_milheiro_agencia,  data_vencimento);
                    compras.add(obj);
                }
            System.out.println("[SISTEMA] Extração completa [2/3] \n" + "=".repeat(50));

        } catch (Exception e) {
            System.out.println("Erro ao extrair dados de compra bonificada!! \n[ERRO] " + e);
        }
        sql = """
            select * from Verificar_Adesao_Boni;
        """;

        System.out.println("[SISTEMA] extraindo dados de adesões bonificadas");
        try (Connection conection = DriverManager.getConnection(url);
            PreparedStatement stmt = conection.prepareStatement(sql);
            ResultSet resultado = stmt.executeQuery()){
                while (resultado.next()) {
                    // Lê linha por linha até não haver mais linhas para ler
                    int id = resultado.getInt("id");
                    String link = resultado.getString("link");
                    String origem = resultado.getString("plataforma_de_origem");
                    String data_vencimento = resultado.getString("data_limite");
                    double valor_milheiro_origem = resultado.getDouble("valor_milheiro_origem");
                    int quantidade_milhas = resultado.getInt("quantidade_milhas");
                    // cria o objeto dos dados extraidos para adicionar a lista
                    Adesao_Boni obj = new Adesao_Boni(id, link, origem, quantidade_milhas,  data_vencimento);
                    adesoes.add(obj);
                }
            System.out.println("[SISTEMA] Extração completa [3/3] \n" + "=".repeat(50));

        } catch (Exception e) {
            System.out.println("Erro ao extrair dados de adesão bonificada!! \n[ERRO] " + e);
        }
            
        
    }
    public static List<Cotacao> extrairCota_BD(){
        List<Cotacao> cotacoes = new ArrayList<>();

        // Extraindo variaveis de ambiente
        Dotenv dotenv = Dotenv.load();
        String USUARIO = dotenv.get("USER");
        String SENHA = dotenv.get("PASSWORD");

        // criando url de conexão ao Banco_da_Millie por meio do app Tailscale;
        String url = "jdbc:mariadb://100.79.171.116:3306/Banco_da_Millie?user=java_user&password=50BMG";
        // Extraindo dados da tabela de promoções de transferência bonificada do banco de dados
        String sql ="""
            SELECT * from cotacoes;
        """;

        try (Connection conection = DriverManager.getConnection(url);
            PreparedStatement stmt = conection.prepareStatement(sql);
            ResultSet resultado = stmt.executeQuery()){
                while (resultado.next()) {
                    // Lê linha por linha até não haver mais linhas para ler
                    int id = resultado.getInt("id");
                    String plataforma = resultado.getString("plataforma");
                    String agencia = resultado.getString("agencia");
                    double valor_min = resultado.getDouble("valor_min");
                    double valor_max = resultado.getDouble("valor_max");
                    // cria o objeto dos dados extraidos para adicionar a lista
                    Cotacao obj = new Cotacao(id, plataforma, agencia, valor_min, valor_max);
                    cotacoes.add(obj);
                }
        } catch (Exception e) {
            System.out.println("Erro ao extrair dados de cotações de milhas!! \n[ERRO] " + e);
        }
        return cotacoes;
    }
    private static boolean avaliarOpcao(String nomeOpcao, double preco_passagem, double preco_passagem_milhas, double milheiro_Opcao) {
        double preco_milheiro_passagem = (preco_passagem/preco_passagem_milhas)*1000.0;
        double custo_opcao = (preco_passagem_milhas/1000.0) * milheiro_Opcao;
        
        // Nota: Se o objetivo é gastar MENOS, a opção é recomendada quando custoOpcao < custoReferencia.
        // Mantive a lógica original (<), mas verifique se o sinal não deveria ser invertido (>).
        boolean recomendada = custo_opcao < preco_passagem;
        String status = recomendada ? "Opção recomendada" : "Opção não recomendada";

        System.out.printf("%s - %s%n\n", nomeOpcao, status);
        System.out.printf("Valor referência do milheiro na passagem %.2fn\n", preco_milheiro_passagem);
        System.out.printf("Valor utilizando %s do milheiro na passagem %.2fn\n", nomeOpcao, milheiro_Opcao);
        System.out.printf("Custo opcao %s = %.2f  |  Custo de referência = %.2f\n", nomeOpcao, custo_opcao, preco_passagem);
        System.out.println("=".repeat(50));
        return recomendada;
    }

}
