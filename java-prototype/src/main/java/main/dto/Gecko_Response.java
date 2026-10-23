package main.dto;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

@JsonIgnoreProperties(ignoreUnknown = true)
public class Gecko_Response{
    private String requestId;
    private String executionId;
    private Boolean notFound;
    private GeckoData data;

    // Getters e Setters
    public String getRequestId() {
        return requestId;
    }
    public void setRequestId(String requestId) {
        this.requestId = requestId;
    }
    public String getexecutionId() {
        return executionId;
    }
    public void setexecutionId(String executionId) {
        this.executionId = executionId;
    }
    public Boolean getNotFound() {
        return notFound;
    }
    public void setNotFound(Boolean notFound) {
        this.notFound = notFound;
    }
    public GeckoData getData() {
        return data;
    }
    public void setData(GeckoData data) {
        this.data = data;
    }
}