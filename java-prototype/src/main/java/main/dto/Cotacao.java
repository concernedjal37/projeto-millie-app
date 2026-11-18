package main.dto;

public class Cotacao {
    private String plataforma;
    private String agencia;
    private double valor_min;
    private double valor_max;
    private String data_atualizada;

    //Getters e Setters
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
    public String getDataAtualizada() {
        return data_atualizada;
    }
    public void setDataAtualizada(String data_atualizada) {
        this.data_atualizada = data_atualizada;
    }


}
