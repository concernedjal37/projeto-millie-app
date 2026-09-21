import 'package:flutter/material.dart';
import 'package:milliefront/views/pages/configuracoes.dart';
import 'package:milliefront/views/pages/login.dart';
import 'package:milliefront/views/pages/perfil.dart';
import 'package:milliefront/views/pages/promocao_e_cotacao.dart';
import 'package:milliefront/views/pages/voos.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});
  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<StatefulWidget> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Container(
          color: Color(0xff303070),
          width: double.infinity,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
               Container(
                color: Color.fromARGB(255, 95, 95, 207),
                height: 200.0,
                width: double.infinity,
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Row(
                      children: [
                        ElevatedButton(onPressed: () {
                          Navigator.push(context, MaterialPageRoute(builder: (context) => Login()));
                        }, child: Text("Butão pra tela de login placeholder")),
                      ],
                    ),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceAround,
                      mainAxisSize: MainAxisSize.max,
                      children: [
                        ElevatedButton(onPressed: () {
                          Navigator.push(context, MaterialPageRoute(builder: (context) => Voos()));
                        },
                        child: Text("Voos")),
                        ElevatedButton(onPressed: () {
                          Navigator.push(context, MaterialPageRoute(builder: (context) => PromocaoECotacao()));
                        }, child: Text("Promoções")),
                        ElevatedButton(onPressed: () {
                          Navigator.push(context, MaterialPageRoute(builder: (context) => PromocaoECotacao()));
                        }, child: Text("Cotações")),
                      ],
                    ),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceAround,
                      mainAxisSize: MainAxisSize.max,
                      children: [
                        Text("Voos",
                        style: TextStyle(
                          color: Colors.white,
                          fontSize: 20,
                        ),
                        ),
                        Text("Promoções",
                        style: TextStyle(
                          color: Colors.white,
                          fontSize: 20,
                        ),
                        ),
                        Text("Cotações",
                        style: TextStyle(
                          color: Colors.white,
                          fontSize: 20,
                        ),
                        ),
                      ],
                    ),
                  ],
                ),
               ),
               Container(
                color: Color(0xff303070),
                width: double.infinity,
               ),
               Container(
                color: Color.fromARGB(255, 95, 95, 207),
                height: 100.0,
                width: double.infinity,
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceAround,
                      mainAxisSize: MainAxisSize.max,
                      children: [
                        ElevatedButton(onPressed: () {
                          Navigator.push(context, MaterialPageRoute(builder: (context) => Perfil()));
                        },
                        child: Text("Perfil")),
                        ElevatedButton(onPressed: () {
                          Navigator.push(context, MaterialPageRoute(builder: (context) => Configuracoes()));
                        }, child: Text("Configurações")),
                      ],
                    ),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceAround,
                      mainAxisSize: MainAxisSize.max,
                      children: [
                        Text("Perfil",
                        style: TextStyle(
                          color: Colors.white,
                          fontSize: 20,
                        ),
                        ),
                        Text("Configurações",
                        style: TextStyle(
                          color: Colors.white,
                          fontSize: 20,
                        ),
                        ),
                      ],
                    ),
                  ],
                ),
               ),
            ],
          ),
        ),
      ),
    );
  }
}
