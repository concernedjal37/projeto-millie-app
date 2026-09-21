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
          color: Color(0xff303070),
          width: double.infinity,
          padding: EdgeInsets.all(50.0),
          child: Container(
            decoration: BoxDecoration(
              color: Color(0xffffffff),
              borderRadius: BorderRadius.circular(25.0),
            ),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
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
                    SwitchListTile.adaptive(
                      title: Text('Switch 1'),
                      value: switch1,
                      onChanged: (bool value) {
                        setState(() {
                          switch1 = value;
                        });
                      },
                    ),
                    SwitchListTile.adaptive(
                      title: Text('Switch 2'),
                      value: switch2,
                      onChanged: (bool value) {
                        setState(() {
                          switch2 = value;
                        });
                      },
                    ),
                    SwitchListTile.adaptive(
                      title: Text('Switch 3'),
                      value: switch3,
                      onChanged: (bool value) {
                        setState(() {
                          switch3 = value;
                        });
                      },
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
