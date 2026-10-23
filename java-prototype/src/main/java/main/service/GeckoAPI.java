package main.service;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import com.fasterxml.jackson.databind.ObjectMapper;
import main.dto.Gecko_Request;
import main.dto.Gecko_Response;

public class GeckoAPI {

    private final HttpClient client = HttpClient.newHttpClient();
    private final ObjectMapper mapper = new ObjectMapper();

    private static final int MAX_TENTATIVAS = 3;
    private static final long TEMPO_ESPERA_MS = 3000; // 3 segundos de intervalo entre chamadas

    public Gecko_Response extrairDados(String apiKey, Gecko_Request requestDto) {
        String jsonBody;
        
        // 1. Serialização do DTO
        try {
            System.out.println("Traduzindo Objeto para arquivo JSON " + "=".repeat(40));
            jsonBody = mapper.writeValueAsString(requestDto);
            System.out.println("JSON enviado: " + jsonBody);
        } catch (IOException e) {
            System.err.println("[ERRO] Falha ao converter DTO para JSON: " + e.getMessage());
            return null; // Retorna null direto se a montagem do JSON falhar
        }

        HttpRequest request = HttpRequest.newBuilder()
                .uri(URI.create("https://api.geckoapi.com.br/v1/extract"))
                .header("Authorization", "Bearer " + apiKey)
                .header("Content-Type", "application/json")
                .header("Accept", "application/json")
                .POST(HttpRequest.BodyPublishers.ofString(jsonBody))
                .build();

        // 2. Loop de tentativas com sleep
        for (int tentativa = 1; tentativa <= MAX_TENTATIVAS; tentativa++) {
            try {
                System.out.printf("Criando e enviando HttpRequest (Tentativa %d/%d)...%n", tentativa, MAX_TENTATIVAS);
                HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());

                System.out.println("Status: " + response.statusCode());
                System.out.println("Body bruto: " + response.body() + "\n" + "=".repeat(40));

                int status = response.statusCode();

                // Caso de Sucesso (HTTP 200 a 299)
                if (status >= 200 && status < 300) {
                    System.out.println("Resposta capturada com sucesso " + "=".repeat(40));
                    return mapper.readValue(response.body(), Gecko_Response.class);
                }

                System.err.printf("[AVISO] Falha na tentativa %d. Status HTTP: %d%n", tentativa, status);

            } catch (IOException e) {
                System.err.printf("[ERRO I/O] Tentativa %d falhou: %s%n", tentativa, e.getMessage());
            } catch (InterruptedException e) {
                System.err.println("[ERRO INTERRUPÇÃO] Requisição interrompida na tentativa " + tentativa);
            }

            // 3. Aplica o sleep apenas se ainda houverem tentativas restantes
            if (tentativa < MAX_TENTATIVAS) {
                try {
                    System.out.println("Aguardando " + (TEMPO_ESPERA_MS / 1000) + " segundos para a próxima tentativa...");
                    Thread.sleep(TEMPO_ESPERA_MS);
                } catch (InterruptedException e) {
                    System.err.println("Sleep interrompido. Prosseguindo...");
                }
            }
        }

        // 4. Se o loop de tentativas esgotar e nada funcionar, retorna null limpo para a Main
        System.err.println("[FALHA FINAL] Todas as " + MAX_TENTATIVAS + " tentativas falharam. Retornando ao menu principal...");
        return null;
    }
}