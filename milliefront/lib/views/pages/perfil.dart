import 'package:flutter/material.dart';
import 'package:milliefront/views/pages/configuracoes.dart';
import 'package:milliefront/views/pages/historico_de_promocoes.dart';
import 'package:milliefront/views/pages/home_page.dart';
import 'package:milliefront/views/pages/notificacoes.dart';
import 'package:milliefront/views/pages/perfil_config.dart';

class Perfil extends StatefulWidget {
  const Perfil({super.key});
  @override
  // ignore: library_private_types_in_public_api
  _PerfilState createState() => _PerfilState();
}

class _PerfilState extends State<StatefulWidget> {
  var _nomeUsuario = "Arthur";
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Container(
          color: Colors.white,
          width: double.infinity,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Flexible(
                child: FractionallySizedBox(
                  heightFactor: 1,
                  widthFactor: 1,
                  child: Container(
                    color: Color.fromARGB(255, 50, 50, 240),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Column(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Row(
                              mainAxisAlignment: MainAxisAlignment.spaceAround,
                              mainAxisSize: MainAxisSize.max,
                              children: [
                                ElevatedButton(
                                  onPressed: () {
                                    Navigator.push(
                                      context,
                                      MaterialPageRoute(
                                        builder: (context) => HomePage(),
                                      ),
                                    );
                                  },
                                  child: Text("Home"),
                                ),
                                ElevatedButton(
                                  onPressed: () {
                                    Navigator.push(
                                      context,
                                      MaterialPageRoute(
                                        builder: (context) => Configuracoes(),
                                      ),
                                    );
                                  },
                                  child: Text("Configurações extras"),
                                ),
                              ],
                            ),
                            Row(
                              mainAxisAlignment: MainAxisAlignment.spaceAround,
                              mainAxisSize: MainAxisSize.max,
                              children: [
                                Text(
                                  "Home",
                                  style: TextStyle(
                                    color: Colors.white,
                                    fontSize: 20,
                                  ),
                                ),
                                Text(
                                  "Configurações extras",
                                  style: TextStyle(
                                    color: Colors.white,
                                    fontSize: 20,
                                  ),
                                ),
                              ],
                            ),
                          ],
                        ),
                        SizedBox(
                          child: Card(
                            color: Color.fromARGB(255, 50, 50, 240),
                            child: CircleAvatar(
                              radius: 100,
                              backgroundImage: AssetImage(
                                'assets/images/OIP.png',
                              ),
                            ),
                          ),
                        ),
                        Text(
                          _nomeUsuario,
                          style: TextStyle(color: Colors.white, fontSize: 20),
                        ),
                      ],
                    ),
                  ),
                ),
              ),
              Flexible(
                child: FractionallySizedBox(
                  heightFactor: 1,
                  widthFactor: 1,
                  child: Container(
                    color: Color(0xff303070),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.start,
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Row(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Icon(Icons.settings, color: Colors.white),
                            ElevatedButton(
                              onPressed: () {
                                Navigator.push(
                                  context,
                                  MaterialPageRoute(
                                    builder: (context) => PerfilConfig(),
                                  ),
                                );
                              },
                              child: Text("Perfil"),
                            ),
                          ],
                        ),
                        Row(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Icon(Icons.settings, color: Colors.white),
                            ElevatedButton(
                              onPressed: () {
                                Navigator.push(
                                  context,
                                  MaterialPageRoute(
                                    builder: (context) => Notificacoes(),
                                  ),
                                );
                              },
                              child: Text("Notificações"),
                            ),
                          ],
                        ),
                        Row(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Icon(Icons.settings, color: Colors.white),
                            ElevatedButton(
                              onPressed: () {
                                Navigator.push(
                                  context,
                                  MaterialPageRoute(
                                    builder: (context) =>
                                        HistoricoDePromocoes(),
                                  ),
                                );
                              },
                              child: Text("Histórico de Promoções"),
                            ),
                          ],
                        ),
                      ],
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
