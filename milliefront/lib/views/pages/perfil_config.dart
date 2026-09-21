import 'package:flutter/material.dart';
import 'package:milliefront/views/pages/login.dart';
import 'package:milliefront/views/pages/perfil.dart';

class PerfilConfig extends StatefulWidget {
  const PerfilConfig({super.key});
  @override
  _PerfilConfigState createState() => _PerfilConfigState();
}

class _PerfilConfigState extends State<StatefulWidget> {
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
                    Text('Perfil', style: TextStyle(fontSize: 18)),
                  ],
                ),
                Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Padding(
                      padding: const EdgeInsets.all(4.0),
                      child: ElevatedButton(onPressed: () {
                        
                      },
                      child: Text('Trocar de nome')),
                    ),
                    Padding(
                      padding: const EdgeInsets.all(4.0),
                      child: ElevatedButton(onPressed: () {
                        
                      }, child: Text('Trocar a foto de perfil')),
                    ),
                    Padding(
                      padding: const EdgeInsets.all(4.0),
                      child: ElevatedButton(onPressed: () {
                        Navigator.push(context, MaterialPageRoute(builder: (context) => Login()));
                      },
                      style: ElevatedButton.styleFrom(
                        backgroundColor: Color(0xffff5050),
                        foregroundColor: Color(0xffeeeeee),
                      ),
                      child: Text('Sair da conta')),
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
