package main.dto;

public class Adesao_Boni {
    private int id;
    private String origem;
    private String destino;
    private double percent_min;
    private double percent_max;
    private int qtd_milhas;
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
    public String getDestino() {
        return destino;
    }
    public void setDestino(String destino) {
        this.destino = destino;
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
    public int getQtdMilhas() {
        return qtd_milhas;
    }
    public void setQtdMilhas(int qtd_milhas) {
        this.qtd_milhas = qtd_milhas;
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
    public Adesao_Boni(int id, String origem, int qtd_milhas, String data_vencimento){
            this.id = id;   
            this.origem = origem;
            this.qtd_milhas = qtd_milhas;
            this.tipo_promo = 3;
            this.data_vencimento = data_vencimento;
        }
}
