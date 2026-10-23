package main.dto;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

@JsonIgnoreProperties(ignoreUnknown = true)
public class GeckoOffers{
    private String brandId;
    private String brandLabel;
    private String cabinClass;
    private int seatsRemaining;
    private GeckoTotal total;

    //Getters e Setters
    public String getBrandId(){
        return brandId;
    }
    public void setBrandId(String brandId){
        this.brandId = brandId;
    }
    public String getBrandLabel(){
        return brandLabel;
    }
    public void setBrandLabel(String brandLabel){
        this.brandLabel = brandLabel;
    }
    public String getCabinClass (){
        return cabinClass;
    }
    public void setCabinClass(String cabinClass){
        this.cabinClass = cabinClass;
    }
    public int getSeatsRemaining(){
        return seatsRemaining;
    }
    public void setSeatsRemaining(int seatsRemaining){
        this.seatsRemaining = seatsRemaining;
    }
    public GeckoTotal getTotal(){
        return total;
    }
    public void setTotal(GeckoTotal total){
        this.total = total;
    }
}
