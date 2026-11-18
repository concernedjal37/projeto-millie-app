package main.dto;

public class Compra_Boni {
    private int id;
    private String origem;
    private double percent_min;
    private double percent_max;
    private double valor_milheiro_agencia;
    private int tipo_promo;
    private String data_vencimento;

    //Getters e Setters
    public int getId(){
        return id;
    }
    public void setId(int id){
        this.id = id;
    }
    public String getOrigem() {
        return origem;
    }
    public void setOrigem(String origem) {
        this.origem = origem;
    }
    public double getPercentMin() {
        return percent_min;
    }
    public void setPercentMin(double percent_min) {
        this.percent_min = percent_min;
    }
    public double getPercentMax() {
        return percent_max;
    }
    public void setPercentMax(double percent_max) {
        this.percent_max = percent_max;
    }
    public double getValorMilhasOrigem() {
        return valor_milheiro_agencia;
    }
    public void setValorMilhasOrigem(double valor_milheiro_agencia) {
        this.valor_milheiro_agencia = valor_milheiro_agencia;
    }
    public int getTipoPromo() {
        return tipo_promo;
    }
    public void setTipoPromo(int tipo_promo) {
        this.tipo_promo = tipo_promo;
    }
    public String getDataVencimento() {
        return data_vencimento;
    }
    public void setDataVencimento(String data_vencimento) {
        this.data_vencimento = data_vencimento;
    }
    public Compra_Boni(int id, String origem,double percent_min, double percent_max, 
        double valor_milheiro_agencia, String data_vencimento){
            this.id = id;   
            this.origem = origem;
            this.percent_min = percent_min;   
            this.percent_max = percent_max;   
            this.valor_milheiro_agencia = valor_milheiro_agencia;
            this.tipo_promo = 2;
            this.data_vencimento = data_vencimento;
    }
}
