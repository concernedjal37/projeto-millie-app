package main.dto;

import java.util.List; 
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

@JsonIgnoreProperties(ignoreUnknown = true)
public class GeckoData {
    private String source;
    private String type;
    private String parser;
    private String url;
    private String requestUrl;
    private String extratedAt;
    private String searchType;
    private String from;
    private String to;
    private String departureDate;
    private String returnDate;
    private int numAdults;
    private int numChildren;
    private int numInfants;
    private Boolean success;
    private int totalResults;
    private List<GeckoItineraries> itineraries;

    // Getters e Setters
    public String getSource() {
        return source;
    }
    public void setSource(String source) {
        this.source = source;
    }
    public String getType() {
        return type;
    }
    public void setType(String type) {
        this.type = type;
    }
    public String getParser() {
        return parser;
    }
    public void setParser(String parser) {
        this.parser = parser;
    }
    public String getUrl() {
        return url;
    }
    public void setUrl(String url) {
        this.url = url;
    }
    public String getRequestId() {
        return requestUrl;
    }
    public void setRequestId(String requestUrl) {
        this.requestUrl = requestUrl;
    }
    public String getExtratedAt() {
        return extratedAt;
    }
    public void setExtratedAt(String extratedAt) {
        this.extratedAt = extratedAt;
    }
    public String getSearchType() {
        return searchType;
    }
    public void setSearchType(String searchType) {
        this.searchType = searchType;
    }
    public String getFrom() {
        return from;
    }
    public void setFrom(String from) {
        this.from = from;
    }
    public String getTo() {
        return to;
    }
    public void setTo(String to) {
        this.to = to;
    }
    public String getDepartureDate() {
        return departureDate;
    }
    public void setDepartureDate(String departureDate) {
        this.departureDate = departureDate;
    }
    public String getReturnDate() {
        return returnDate;
    }
    public void setReturnDate(String returnDate) {
        this.returnDate = returnDate;
    }
    public int getNumAdults() {
        return numAdults;
    }
    public void setNumAdults(int numAdults) {
        this.numAdults = numAdults;
    }
    public int getNumChildren() {
        return numChildren;
    }
    public void setNumChildren(int numChildren) {
        this.numChildren = numChildren;
    }
    public int getNumInfants() {
        return numInfants;
    }
    public void setNumInfants(int numInfants) {
        this.numInfants = numInfants;
    }
    public Boolean getSuccess() {
        return success;
    }
    public void setSuccess(Boolean success) {
        this.success = success;
    }
    public int getTotalResults(){
        return totalResults;
    }
    public void setTotalResults(int totalResults){
        this.totalResults = totalResults;
    }
    public List<GeckoItineraries> getItineraries() {
        return itineraries;
    }
    public void setItineraries(List<GeckoItineraries> itineraries) {
        this.itineraries = itineraries;
    }
}
