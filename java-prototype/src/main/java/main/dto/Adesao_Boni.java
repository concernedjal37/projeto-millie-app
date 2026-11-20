package main.dto;

public class Adesao_Boni {
    private int id;
    private String link;
    private String origem;
    private int qtd_milhas;
    private int tipo_promo;
    private String data_vencimento;
    // Contrutor Padrão
    public Adesao_Boni(){
            this.id = 0;   
            this.link = null;
            this.origem = null;
            this.qtd_milhas = 0;
            this.tipo_promo = 0;
            this.data_vencimento = null;
        }

    // Contrutor Extração Banco de dados
    public Adesao_Boni(int id,String link, String origem, int qtd_milhas, String data_vencimento){
        this.id = id;   
        this.link = link;
        this.origem = origem;
        this.qtd_milhas = qtd_milhas;
        this.tipo_promo = 3;
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
    public boolean isEmpty() {
        return this.id == 0
            && (this.link == null || this.link.isBlank())
            && (this.origem == null || this.origem.isBlank())
            && this.tipo_promo == 0
            && (this.data_vencimento == null || this.data_vencimento.isBlank());
    }

    public void printAdesao(){
        if (isEmpty()) {
            System.out.println("[Transferência vazia]");
            return;
        }
        System.out.println("==================================================");
        System.out.printf("id: %d | From: %s | ", this.id, this.origem);
        System.out.printf("Mihas: %d\n", this.qtd_milhas);
        System.out.println("==================================================");
    }

}
