package main.dto;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

@JsonIgnoreProperties(ignoreUnknown = true)
public class GeckoFlight{
    private String airlineCode;
    private String flightNumber;
    private String equipamentCode;

    // Getters e Setters
    public String getAirline(){return airlineCode;}
    public void setAirline(String airlineCode){this.airlineCode = airlineCode;}
    public String getFlightNumber(){return flightNumber;}
    public void setFlightNumber(String flightNumber){this.flightNumber = flightNumber;}
    public String getEquipamentCode(){return equipamentCode;}
    public void setEquipamentCode(String equipamentCode){this.equipamentCode = equipamentCode;}
}