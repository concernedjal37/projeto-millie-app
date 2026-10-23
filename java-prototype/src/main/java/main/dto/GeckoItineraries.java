package main.dto;

import java.util.List;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

@JsonIgnoreProperties(ignoreUnknown = true)
public class GeckoItineraries{
    private String id;
    private int position;
    private String origin;
    private String destination;
    private String departure;
    private String arrival;
    private int stopCount;
    private String duration;
    private List<GeckoSegments> segments;
    private List<GeckoOffers> offers;
    private GeckoCheapestOffer cheapestOffer;

    // Getters e Setters
    public String getId() {return id;}
    public void setId(String id) {this.id = id;}

    public int getPosition() {
        return position;
    }
    public void setPosition(int position) {
        this.position = position;
    }
    public String getOrigin() {
        return origin;
    }
    public void setOrigin(String origin) {
        this.origin = origin;
    }
    public String getDestination() {
        return destination;
    }
    public void setDestination(String destination) {
        this.destination = destination;
    }
    public String getDeparture() {
        return departure;
    }
    public void setDeparture(String departure) {
        this.departure = departure;
    }
    public String getArrival() {
        return arrival;
    }
    public void setArrival(String arrival) {
        this.arrival = arrival;
    }
    public int getStopCount() {
        return stopCount;
    }
    public void setStopCount(int stopCount) {
        this.stopCount = stopCount;
    }
    public String getDuration() {
        return duration;
    }
    public void setDuration(String duration) {
        this.duration = duration;
    }
    public List<GeckoSegments> getSegments() {
        return segments;
    }
    public void setSegments(List<GeckoSegments> segments) {
        this.segments = segments;
    }
    public List<GeckoOffers> getGeckoOffers() {
        return offers;
    }
    public void setOffers(List<GeckoOffers> offers) {
        this.offers = offers;
    }
    public GeckoCheapestOffer getCheapestOffer() {
        return cheapestOffer;
    }
    public void setCheapestOffer(GeckoCheapestOffer cheapestOffer) {
        this.cheapestOffer = cheapestOffer;
    }
}
