package com.example;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.ResultSet;
import java.sql.Statement;

//import org.mariadb.jdbc.Statement;

public class Main {
    public static void main(String[] args) throws Exception{
        try{
            Connection connection = DriverManager.getConnection("jdbc:mariadb://localhost:3306/Banco_da_Millie?user=root&password=50BMG");
            Statement algo =  connection.createStatement();
            ResultSet resultado = algo.executeQuery("select * from Usuarios");
            while (resultado.next()) {
                System.out.print("ID: " + resultado.getInt("id"));
                System.out.print(" // nome: " + resultado.getNString("nome"));
                System.out.print(" // e_mail: " + resultado.getNString("e_mail"));
                System.out.print(" // cep: " + resultado.getNString("cep"));
                System.out.print(" // bairro: " + resultado.getNString("bairro"));
                System.out.print(" // cidade: " + resultado.getNString("cidade"));
                System.out.print(" // estado: " + resultado.getNString("estado"));
                System.out.println(" // pais: " + resultado.getNString("pais"));
                //System.out.println("Deu certo");
            }
            connection.close();
        }
        catch (Exception e){
            System.out.println(e.getMessage());
        }
    }
}