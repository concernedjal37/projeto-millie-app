package main.dto;

import java.util.List;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

@JsonIgnoreProperties(ignoreUnknown = true)
public class GeckoSegments{
        private String origin;
        private String destination;
        private String departure;
        private String arrival;
        private String duration;
        private List<GeckoFlight> flight;

        // Getters e Setters
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
        public String getDuration() {
            return duration;
        }
        public void setDuration(String duration) {
            this.duration = duration;
        }
        public List<GeckoFlight> getFlights() {
            return flight;
        }
        public void setFlights(List<GeckoFlight> flight) {
            this.flight = flight;
        }
    }