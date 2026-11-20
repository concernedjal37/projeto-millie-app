package main.dto;


public class Cotacao {
    private int id;
    private String plataforma;
    private String agencia;
    private double valor_min;
    private double valor_max;
    // Construtor padrão
    public Cotacao(){
        this.id = 0;   
        this.plataforma = null;
        this.agencia = null;   
        this.valor_min = 0.0;   
        this.valor_max = 0.0;   
    }
    // Construtor para extração do banco de dados
    public Cotacao(int id, String plataforma, String agencia, double valor_min, double valor_max){
        this.id = id;   
        this.plataforma = plataforma;
        this.agencia = agencia;   
        this.valor_min = valor_min;   
        this.valor_max = valor_max;   
    }

    //Getters e Setters
    public int getId(){
        return id;
    }
    public void setId(int id){
        this.id = id;
    }
    public String getPlataforma() {
        return plataforma;
    }
    public void setPlataforma(String plataforma) {
        this.plataforma = plataforma;
    }
    public String getAgencia() {
        return agencia;
    }
    public void setAgencia(String agencia) {
        this.agencia = agencia;
    }
    public double getValorMin() {
        return valor_min;
    }
    public void setValorMin(double valor_min) {
        this.valor_min = valor_min;
    }
    public double getValorMax() {
        return valor_max;
    }
    public void setValorMax(double valor_max) {
        this.valor_max = valor_max;
    }
    public boolean isEmpty() {
        return this.id == 0
            && (this.agencia == null || this.agencia.isBlank())
            && (this.plataforma == null || this.plataforma.isBlank())
            && this.valor_max == 0.0
            && this.valor_min == 0.0;
    }

    public void printCota(){
        if (isEmpty()) {
            System.out.println("[Transferência vazia]");
            return;
        }
        System.out.println("==================================================");
        System.out.printf("id: %d | Plataforma: %s | Agencia: %s | ", this.id, this.plataforma, this.agencia);
        System.out.printf("Min: %.2f | Máx: %.2f\n", this.valor_min, this.valor_max);
        System.out.println("==================================================");
    }

}
