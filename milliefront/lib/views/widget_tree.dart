import 'package:flutter/material.dart';
import 'package:milliefront/views/pages/historico_de_promocoes.dart';
import 'package:milliefront/views/pages/home_page.dart';
import 'package:milliefront/views/pages/notificacoes.dart';
import 'package:milliefront/views/pages/perfil_config.dart';
import 'package:milliefront/views/pages/login.dart';
import 'package:milliefront/views/pages/perfil.dart';
import 'package:milliefront/views/pages/configuracoes.dart';
import 'package:milliefront/views/pages/promocao_e_cotacao.dart';
import 'package:milliefront/views/pages/voos.dart';
import 'package:milliefront/widgets/navbar_widget.dart';

List<Widget> pages = [
  HomePage(),
  Voos(),
  PromocaoECotacao(),
  Login(),
  Perfil(),
  Configuracoes(),
  PerfilConfig(),
  Notificacoes(),
  HistoricoDePromocoes(),
];

class WidgetTree extends StatelessWidget {
  const new({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(),
      drawer: Drawer(
        child: Column(
         children: [
            DrawerHeader(child: Text('Millie')),
            ListTile(
              leading: Icon(Icons.login),
              title: Text('Login'),
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => Login()),
                );
              },
            ),
            ListTile(
              leading: Icon(Icons.person),
              title: Text('Perfil'),
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => Perfil()),
                );
              },
            ),
            ListTile(
              leading: Icon(Icons.settings),
              title: Text('Configurações'),
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => Configuracoes()),
                );
              },
            ),
          ],
        ),
      ),
      body: pages.elementAt(0),
      bottomNavigationBar: NavbarWidget(),
    );
  }
}