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
import java.sql.SQLException;

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
            GeckoItineraries menorPreco = encontraMenor(responseDTO.getData().getItineraries());

            double precoDinheiro = menorPreco.getCheapestOffer().getTotal().getAmount();
            String moeda = menorPreco.getCheapestOffer().getTotal().getCurrency();

            System.out.println("=".repeat(40) + "\nViagem mais econômica (Dinheiro)");
            System.out.println("Origem: " + menorPreco.getOrigin());
            System.out.println("Destino: " + menorPreco.getDestination());
            System.out.println("Duração: " + formatDuration(menorPreco.getDuration()));
            System.out.println("Valor: " + moeda + " " + String.format("%.2f", precoDinheiro));

            // ====================================================================
            // CÁLCULO E COMPARAÇÃO DE MODALIDADES DE PAGAMENTO
            // ====================================================================
            
            // Dados da passagem em milhas (simulação/banco)
            double precoMilhas = 24000.0;
            double milheirosNecessarios = precoMilhas / 1000.0;

            // Simulação de parâmetros vindos do banco de dados/promoções
            double cotaValorMilheiro = 23.50; // Cotação mercado secundário
            
            double precoCompraBase = 70.00;   // Preço padrão do milheiro
            double bonusCompraPercent = 100.0; // 100% de bônus na compra
            
            double cpmOrigemBanco = 35.00;    // Custo base no banco/cartão
            double bonusTransfPercent = 80.0;  // 80% de bônus na transferência

            // 1. Cálculo do custo total em cada modalidade (R$)
            double custoDinheiro = precoDinheiro;

            double cpmCotacao = cotaValorMilheiro;
            double custoCotacao = milheirosNecessarios * cpmCotacao;

            double cpmCompraBonus = precoCompraBase / (1 + (bonusCompraPercent / 100.0));
            double custoCompraBonus = milheirosNecessarios * cpmCompraBonus;

            double cpmTransfBonus = cpmOrigemBanco / (1 + (bonusTransfPercent / 100.0));
            double custoTransfBonus = milheirosNecessarios * cpmTransfBonus;

            // 2. Determinação da modalidade mais barata
            double menorCusto = custoDinheiro;
            String melhorOpcao = "Pagamento em Dinheiro no site";

            if (custoCotacao < menorCusto) {
                menorCusto = custoCotacao;
                melhorOpcao = "Compra de Milhas via Cotação";
            }
            if (custoCompraBonus < menorCusto) {
                menorCusto = custoCompraBonus;
                melhorOpcao = "Compra Bonificada (" + (int) bonusCompraPercent + "% bônus)";
            }
            if (custoTransfBonus < menorCusto) {
                menorCusto = custoTransfBonus;
                melhorOpcao = "Transferência Bonificada (" + (int) bonusTransfPercent + "% bônus)";
            }

            // 3. Exibição do Comparativo
            System.out.println("\n" + "=".repeat(40));
            System.out.println("RESUMO COMPARATIVO DE PREÇOS:");
            System.out.printf("- Dinheiro direto: R$ %.2f%n", custoDinheiro);
            System.out.printf("- Cotação (CPM R$ %.2f): R$ %.2f%n", cpmCotacao, custoCotacao);
            System.out.printf("- Compra Bonificada (CPM R$ %.2f): R$ %.2f%n", cpmCompraBonus, custoCompraBonus);
            System.out.printf("- Transferência Bonificada (CPM R$ %.2f): R$ %.2f%n", cpmTransfBonus, custoTransfBonus);
            System.out.println("-".repeat(40));
            System.out.printf(">>> MELHOR OPÇÃO: %s por R$ %.2f%n", melhorOpcao, menorCusto);
            System.out.println("=".repeat(40));
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
                        case "CL":
                            System.out.println("Classic");
                        case "FL":
                            System.out.println("Flex");
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
        Long minutes = duration.toMinutes();

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
        Dotenv dotenv = Dotenv.load();
        String USUARIO = dotenv.get("USER");
        String SENHA = dotenv.get("PASSWORD");

        // criando url de conexão ao Banco_da_Millie por meio do app Tailscale;
        String url = "jdbc:mariadb://" + HOST_TAILSCALE + ":" + PORTA + "/" + BANCO;
        // Extraindo dados da tabela de promoções de transferência bonificada do banco de dados
        String sql ="""
            SELECT * FROM VERIFICAR_TRANSFERENCIA_BONI;
        """;

        try (Connection conection = DriverManager.getConnection(url,USUARIO,SENHA);
            PreparedStatement stmt = conection.prepareStatement(sql);
            ResultSet rs = stmt.executeQuery()){
                while (rs.next()) {
                    // Lê linha por linha até não haver mais linhas para ler
                    int id = rs.getInt("id_promocoes");
                    String origem = rs.getString("plataforma_de_origem");
                    String destino = rs.getString("plataforma_de_destino");
                    double percent_min = rs.getDouble("percentual_MIN");
                    double percent_max = rs.getDouble("percentual_MAX");
                    double valor_milheiro_agencia = rs.getDouble("valor_milheiro_agencia");
                    String data_vencimento = rs.getString("data_limite");
                    // cria o objeto dos dados extraidos para adicionar a lista
                    Transferencia_Boni obj = new Transferencia_Boni(id,origem,destino,percent_min,percent_max,valor_milheiro_agencia,data_vencimento);
                    transferencias.add(obj);
                }
        } catch (Exception e) {
            System.out.println("Erro ao extrair dados de transferência bonificada!! \n[ERRO] " + e);
            // TODO: handle exception
        }
        sql = """
            SELECT * FROM VERIFICAR_COMPRA_BONI;
        """;
        try (Connection conection = DriverManager.getConnection(url,USUARIO,SENHA);
            PreparedStatement stmt = conection.prepareStatement(sql);
            ResultSet rs = stmt.executeQuery()){
                while (rs.next()) {
                    // Lê linha por linha até não haver mais linhas para ler
                    int id = rs.getInt("id_promocoes");
                    String origem = rs.getString("plataforma_de_origem");
                    double percent_min = rs.getDouble("percentual_MIN");
                    double percent_max = rs.getDouble("percentual_MAX");
                    double valor_milheiro_agencia = rs.getDouble("valor_milheiro_agencia");
                    String data_vencimento = rs.getString("data_limite");
                    // cria o objeto dos dados extraidos para adicionar a lista
                    Compra_Boni obj = new Compra_Boni(id, origem, percent_min, percent_max, valor_milheiro_agencia,  data_vencimento);
                    compras.add(obj);
                }
        } catch (Exception e) {
            System.out.println("Erro ao extrair dados de transferência bonificada!! \n[ERRO] " + e);
        }
        sql = """
            SELECT * FROM VERIFICAR_ADESAO_BONI;
        """;
        try (Connection conection = DriverManager.getConnection(url,USUARIO,SENHA);
            PreparedStatement stmt = conection.prepareStatement(sql);
            ResultSet rs = stmt.executeQuery()){
                while (rs.next()) {
                    // Lê linha por linha até não haver mais linhas para ler
                    int id = rs.getInt("id_promocoes");
                    String origem = rs.getString("plataforma_de_origem");
                    int qtd_milhas = rs.getInt("qtd_milhas");
                    String data_vencimento = rs.getString("data_limite");
                    // cria o objeto dos dados extraidos para adicionar a lista
                    Adesao_Boni obj = new Adesao_Boni(id, origem, qtd_milhas,  data_vencimento);
                    adesoes.add(obj);
                }
        } catch (Exception e) {
            System.out.println("Erro ao extrair dados de transferência bonificada!! \n[ERRO] " + e);
        }
            
        
    }
}
