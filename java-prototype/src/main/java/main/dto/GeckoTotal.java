package main.dto;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

@JsonIgnoreProperties(ignoreUnknown = true)
public class GeckoTotal{
    private String currency;
    private double amount;

    //Getters e Setters
    public String getCurrency(){return currency;}
    public void setCurrency(String currency){this.currency = currency;}
    public double getAmount(){return amount;}
    public void setAmount(double amount){this.amount = amount;}
}