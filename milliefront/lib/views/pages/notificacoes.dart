import 'package:flutter/material.dart';
import 'package:milliefront/views/pages/perfil.dart';

class Notificacoes extends StatefulWidget {
  const Notificacoes({super.key});
  @override
  _NotificacoesState createState() => _NotificacoesState();
}

class _NotificacoesState extends State<StatefulWidget> {
  bool switch1 = false;
  bool switch2 = false;
  bool switch3 = false;
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Container(
          color: Color.fromARGB(255, 30, 30, 130),
          width: double.infinity,
          padding: EdgeInsets.all(50.0),
          child: Container(
            decoration: BoxDecoration(
              color: Color(0xffffffff),
              borderRadius: BorderRadius.circular(25.0),
            ),
            padding: EdgeInsets.all(10.0),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.start,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    BackButton(
                      onPressed: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(builder: (context) => Perfil()),
                        );
                      },
                    ),
                    Text('Notificações', style: TextStyle(fontSize: 18)),
                  ],
                ),
                Column(
                  children: [
                    Padding(
                      padding: const EdgeInsets.all(4.0),
                      child: SwitchListTile.adaptive(
                        title: Text('Notificações de recomendações de voos',
                        style: TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                        ),
                        ),
                        value: switch1,
                        onChanged: (bool value) {
                          setState(() {
                            switch1 = value;
                          });
                        },
                      ),
                    ),
                    Padding(
                      padding: const EdgeInsets.all(4.0),
                      child: SwitchListTile.adaptive(
                        title: Text('Notificações de recomendações de promoções e cotações',
                        style: TextStyle(
                          fontSize: 16,
                          fontWeight: FontWeight.bold,
                        ),
                        ),
                        value: switch2,
                        onChanged: (bool value) {
                          setState(() {
                            switch2 = value;
                          });
                        },
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
