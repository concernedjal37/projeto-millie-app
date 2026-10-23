package main;

import java.io.IOException;
import java.time.Duration;
import java.util.List;
import io.github.cdimascio.dotenv.Dotenv;
import java.util.Scanner;

import main.dto.GeckoItineraries;
import main.dto.GeckoOffers;
import main.dto.Gecko_Request;
import main.dto.Gecko_Response;
import main.service.GeckoAPI;

public class Main {
    private static final Object lock = new Object();
    public static void main(String[] args) throws IOException, InterruptedException {
        System.out.println("Iniciando programa");
        // 1. THREAD de Trabalho (contínuo)
        Thread workerThread = new Thread(() -> {
            while(true){
                // Script de aguarde de gatilho -> "Start"
                synchronized (lock) {
                    try {
                        System.out.println("[worker] em stand by. aguardando star...");
                        lock.wait(); // Execução pause até receber start
                    } catch (InterruptedException e) {
                        Thread.currentThread().interrupt();
                        break;
                    }     
                }
                // Script contínuo do código a ser executado
                //Extração de dados do GeckoAPI "passagens aéreas"
                Gecko_Response responseDTO = scrapingData();
                if(responseDTO.getData()!= null && responseDTO.getData().getItineraries() != null){ 
                    // Função de listagem de todos os resultados encontrados no Scrapping
                    listItineraries(responseDTO.getData().getItineraries());
                    
                    // Instanciando Objeto para receber menor preço de itinerário
                    GeckoItineraries menorPreco = encontraMenor(responseDTO.getData().getItineraries());
                    
                    System.out.println("=".repeat(40) + "\nViagem mais econômica");
                    System.out.println("Fonte: GOL");
                    System.out.println("Origem: " + menorPreco.getOrigin());
                    System.out.println("Destino: " + menorPreco.getDestination());
                    System.out.println("Duração: " + formatDuration(menorPreco.getDuration()));
                    System.out.println("Moeda: " + menorPreco.getCheapestOffer().getTotal().getCurrency());
                    System.out.println("Origem: " + menorPreco.getCheapestOffer().getTotal().getAmount());

                    // Comparação com valor de cotação e compra bonificada de milhas
                    // Valores Teste (Falta vinculação do banco de dados)

                    //Simulação valores teste de cotação de milhas da smiles
                    String cota_plataforma = "voegol";
                    double cota_valor = 23.5;
                    System.out.println("Preço cotação" + cota_plataforma + "R$" + String.format("%.2f", cota_valor));

                    String compra_bonus_plataforma = "voegol";
                    // Simulação de valores para preço da passagem pesquisada na API em milhas
                    double preco_milhas = 24000.0;
                    String plataforma = responseDTO.getData().getSource().split("\\.")[0];

                    // Calculando preco por milha da passagem pesquisada na API
                    double preco_por_milheiro = (menorPreco.getCheapestOffer().getTotal().getAmount() / preco_milhas) * 1000.0;
                    // Realizando comparações
                    switch (plataforma) {
                        case "voegol":

                            if (preco_por_milheiro <= cota_valor) {
                                System.out.println("Comprar diretamente no site da gol é mais barato");
                            }else{
                                System.out.println("Compre as milhas pela contação é mais barato");
                            }

                            break;
                        case "smiles":

                            if (preco_por_milheiro <= cota_valor) {
                                System.out.println("Comprar diretamente no site da gol é mais barato");
                            }else{
                                System.out.println("Compre as milhas pela contação é mais barato");
                            }

                            break;
                        case "azul":

                            if (preco_por_milheiro <= cota_valor) {
                                System.out.println("Comprar diretamente no site da gol é mais barato");
                            }else{
                                System.out.println("Compre as milhas pela contação é mais barato");
                            }

                            break;
                        default:
                            throw new AssertionError();
                    }
                }
                // Comparação com valor de Compra Bonificada



                // Comparação com valor em Transferência Bonificada

            }
        });
        workerThread.start();

        // 2. THREAD de Controle (gatilho Start)
        Scanner scanner = new Scanner(System.in);
        System.out.println("Digite 'start' para iniciar / 'finish' para encerrar");

        // Condicionamento para "Start" ou "Finish" do programa
        while (true){
            String comando = scanner.nextLine();
            if(comando.equalsIgnoreCase("start")){
                disparaStart();
            }else if(comando.equalsIgnoreCase("finish")){
                System.err.println("Encerrar sistema...");
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
         try {
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
            String apiKey = "pk_live_Ew6DYPeqLQmEfWAisS2DTFoMGXtgMKLK"; 
            // Enviando Request para Gecko API
            System.out.println("Iniciando scraping...");
            Gecko_Response response = geckoAPI.extrairDados(myApiKey, requestDto); // Função de scrapping de dados API

            // Imprimindo Resposta "Response" recebida do scraping de dados
            System.out.println("Request ID: " + response.getRequestId());
            System.out.println("Execution Time: " + response.getexecutionId());
            System.out.println("Not Found: " + response.getNotFound());

            // Condicionamento para manipulação de dados
            if (Boolean.TRUE.equals(response.getNotFound())){ // Responsta não encontrou dados para os parâmetros de request
                System.out.println("Nenhum resultado encontrado para a pesquisa.");
                return response;

            }else if(response.getData() != null) {// Resposta com dados encontrados
                System.out.println("Dados extraídos com sucesso:");
                System.out.println("Fonte de Pesquisa: " + response.getData().getSource());
                System.out.println("Tipo de Pesquisa: " + response.getData().getSearchType());
                return response;

            }else{ // Resposta não apresentou dado algum (provável erro no scrapping)
                System.out.println("A resposta veio sem dados.");
                return response;
            }
             
        } catch (IOException e) {
            System.out.println("Erro de IO: " + e.getMessage());
        } catch (InterruptedException e) {
            System.out.println("Erro de Interrupção: " + e.getMessage());
        }

        return null;

    }
    public static void setRequest(GeckoAPI geckoAPI, Gecko_Request requestDto){
        System.out.println("Estabelecendo Objeto de Request");
        System.out.println("""
                               Set Valores de Objeto Request
                               """ + "=".repeat(40));
            requestDto.setTarget("voegol.com.br");
            requestDto.setType("plp");
            requestDto.setFrom("CNF");
            requestDto.setTo("GRU");
            requestDto.setDepartureDate("2026-10-19");
            requestDto.setReturnDate("2026-10-26");
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

}
