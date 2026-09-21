import 'package:flutter/material.dart';
import 'package:milliefront/views/pages/home_page.dart';

class Configuracoes extends StatefulWidget{
  const Configuracoes({super.key});
  @override
  _ConfiguracoesState createState() => _ConfiguracoesState();
}
class _ConfiguracoesState extends State<StatefulWidget> {
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
              mainAxisAlignment: MainAxisAlignment.start,
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    BackButton(onPressed: () {
                        Navigator.push(context, MaterialPageRoute(builder: (context) => HomePage()));
                      },
                    ),
                    Text('Configurações',
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