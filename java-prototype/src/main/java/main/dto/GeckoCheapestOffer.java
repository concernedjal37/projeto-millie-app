package main.dto;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;

@JsonIgnoreProperties(ignoreUnknown = true)
public class GeckoCheapestOffer{
    private String brandId;
    private GeckoTotal total;

    //Getters e Setters
    public String getBrandId(){return brandId;}
    public void setBrandId(String brandId){this.brandId = brandId;}
    public GeckoTotal getTotal(){return total;}
    public void setTotal(GeckoTotal total){this.total = total;}
}