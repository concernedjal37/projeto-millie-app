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

    public Gecko_Response extrairDados(String api_Key, Gecko_Request requestDto) throws IOException, InterruptedException {
        try{
            System.out.println("Traduzindo Objeto para arquivo JSON" + "=".repeat(40));
            String jsonBody = mapper.writeValueAsString(requestDto);
            System.out.println("JSON enviado: " + jsonBody);
            System.out.println("Criando HttpRequest...");
            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create("https://api.geckoapi.com.br/v1/extract"))
                    .header("Authorization", "Bearer " + api_Key)
                    .header("Content-Type", "application/json")
                    .header("Accept","application/json")
                    .POST(HttpRequest.BodyPublishers.ofString(jsonBody))
                    .build();

            HttpResponse<String> response = client.send(request, HttpResponse.BodyHandlers.ofString());
            System.out.println("""
                               HttpRequest Criado
                               """ + "=".repeat(40));
            
            System.out.println("Status: " + response.statusCode());
            System.out.println("Body bruto: " + response.body() + "\n" + "=".repeat(40));

            if(response.statusCode() >= 200 && response.statusCode() < 300){
                System.out.println("""
                                   Resposta capturada com sucesso
                                   """ + "=".repeat(40));
                System.out.println("Status: " + response.statusCode());
                System.out.println("Body bruto: " + response.body() + "\n" + "=".repeat(40));
                
                return mapper.readValue(response.body(), Gecko_Response.class);
            } else {
                throw new RuntimeException("Erro na API Gecko: " + response.statusCode() + " | " + response.body());            }
        }catch (IOException e){
            System.out.println("Erro de IO: " + e.getMessage());
            throw e;
        }
    }
}
