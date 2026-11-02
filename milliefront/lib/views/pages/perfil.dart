import 'package:flutter/material.dart';
import 'package:milliefront/views/pages/historico_de_promocoes.dart';
import 'package:milliefront/views/pages/notificacoes.dart';
import 'package:milliefront/views/pages/perfil_config.dart';
import 'package:milliefront/views/widget_tree.dart';

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
          color: Color.fromARGB(255, 30, 30, 130),
          padding: EdgeInsets.all(50.0),
          child: Container(
            padding: EdgeInsets.all(10.0),
            decoration: BoxDecoration(
              color: Color(0xffffffff),
              borderRadius: BorderRadius.circular(25.0),
            ),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Flexible(
                  child: SizedBox(
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        Column(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Row(
                              mainAxisAlignment: MainAxisAlignment.start,
                              mainAxisSize: MainAxisSize.max,
                              children: [
                                BackButton(
                                  onPressed: () {
                                    Navigator.push(
                                      context,
                                      MaterialPageRoute(
                                        builder: (context) => WidgetTree(),
                                      ),
                                    );
                                  },
                                ),
                                Text('Perfil', style: TextStyle(fontSize: 18)),
                              ],
                            ),
                          ],
                        ),
                        SizedBox(
                          child: Card(
                            color: Color.fromARGB(255, 255, 255, 255),
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
                          style: TextStyle(color: Colors.black, fontSize: 20),
                        ),
                      ],
                    ),
                  ),
                ),
                Flexible(
                  child: SizedBox(
                    child: Container(
                      padding: EdgeInsets.all(10.0),
                      child: Column(
                        mainAxisAlignment: MainAxisAlignment.start,
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Icon(Icons.settings, color: Colors.black),
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
                              Icon(Icons.settings, color: Colors.black),
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
                              Icon(Icons.settings, color: Colors.black),
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
      ),
    );
  }
}
