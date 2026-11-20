package main.dto;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

@JsonIgnoreProperties(ignoreUnknown = true)
public class GeckoTotal{
    private String currency;
    private double amount;
    private double miles;

    //Getters e Setters
    public double getMiles(){return miles;}
    public void set(double miles){this.miles = miles;}
    public String getCurrency(){return currency;}
    public void setCurrency(String currency){this.currency = currency;}
    public double getAmount(){return amount;}
    public void setAmount(double amount){this.amount = amount;}
}