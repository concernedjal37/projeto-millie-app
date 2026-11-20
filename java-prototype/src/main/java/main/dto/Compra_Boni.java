package main.dto;

public class Compra_Boni {
    private int id;
    private String link;
    private String origem;
    private double percent_min;
    private double percent_max;
    private double valor_milheiro_origem;
    private int tipo_promo;
    private String data_vencimento;
    //Contrutor padrão
    public Compra_Boni(){
        this.id = 0;  
        this.link = null; 
        this.origem = null;
        this.percent_min = 0.0;   
        this.percent_max = 0.0;   
        this.valor_milheiro_origem = 0.0;
        this.tipo_promo = 0;
        this.data_vencimento = null;

    }
    //Contrutor Extração banco de dados
    public Compra_Boni(int id, String link, String origem,double percent_min, double percent_max, 
        double valor_milheiro_origem, String data_vencimento){
            this.id = id;  
            this.link = link; 
            this.origem = origem;
            this.percent_min = percent_min;   
            this.percent_max = percent_max;   
            this.valor_milheiro_origem = valor_milheiro_origem;
            this.tipo_promo = 2;
            this.data_vencimento = data_vencimento;
    }

    //Getters e Setters
    public int getId(){
        return id;
    }
    public void setId(int id){
        this.id = id;
    }
    public String getLink(){
        return link;
    }
    public void setLink(String link){
        this.link = link;
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
        return valor_milheiro_origem;
    }
    public void setValorMilhasOrigem(double valor_milheiro_origem) {
        this.valor_milheiro_origem = valor_milheiro_origem;
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
    public boolean isEmpty() {
        return this.id == 0
            && (this.link == null || this.link.isBlank())
            && (this.origem == null || this.origem.isBlank())
            && this.percent_min == 0.0
            && this.percent_max == 0.0
            && this.valor_milheiro_origem == 0.0
            && this.tipo_promo == 0
            && (this.data_vencimento == null || this.data_vencimento.isBlank());
    }

    public void printCompra(){
        if (isEmpty()) {
            System.out.println("[Transferência vazia]");
            return;
        }
        System.out.println("==================================================");
        System.out.printf("id: %d | From: %s | ", this.id, this.origem);
        System.out.printf("Min: %.2f | Máx: %.2f\n", this.percent_min, this.percent_max);
        System.out.println("==================================================");
    }

}
