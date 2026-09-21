import 'package:flutter/material.dart';
import 'package:milliefront/views/pages/perfil.dart';

class PerfilConfig extends StatefulWidget{
  const PerfilConfig({super.key});
  @override
  _PerfilConfigState createState() => _PerfilConfigState();
}
class _PerfilConfigState extends State<StatefulWidget> {
  @override
  Widget build(BuildContext context){
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
                    BackButton(onPressed: () {
                        Navigator.push(context, MaterialPageRoute(builder: (context) => Perfil()));
                      },
                    ),
                    Text('Perfil',
                    style: TextStyle(
                      fontSize: 18,
                    ),
                    )
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