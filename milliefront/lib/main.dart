import 'package:flutter/material.dart';
import 'package:milliefront/views/pages/configuracoes.dart';
import 'package:milliefront/views/pages/historico_de_promocoes.dart';
import 'package:milliefront/views/pages/home_page.dart';
import 'package:milliefront/views/pages/login.dart';
import 'package:milliefront/views/pages/notificacoes.dart';
import 'package:milliefront/views/pages/perfil.dart';
import 'package:milliefront/views/pages/perfil_config.dart';
import 'package:milliefront/views/pages/promocao_e_cotacao.dart';
import 'package:milliefront/views/pages/voos.dart';


List<Widget> pages = [
  HomePage(),
  Login(),
  Perfil(),
  Voos(),
  PromocaoECotacao(),
  Configuracoes(),
  PerfilConfig(),
  Notificacoes(),
  HistoricoDePromocoes(),
];

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Millie Arthur',
      theme: ThemeData(
        colorScheme: .fromSeed(seedColor: Colors.deepPurple),
      ),
      home: HomePage(),
    );
  }
}

