import 'package:flutter/material.dart';
import 'package:milliefront/views/pages/perfil.dart';

class HistoricoDePromocoes extends StatefulWidget {
  const HistoricoDePromocoes({super.key});
  @override
  _HistoricoDePromocoesState createState() => _HistoricoDePromocoesState();
}

class _HistoricoDePromocoesState extends State<StatefulWidget> {
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
                    Padding(
                      padding: const EdgeInsets.all(4.0),
                      child: Text(
                        'Histórico de promoções',
                        style: TextStyle(fontSize: 18),
                      ),
                    ),
                  ],
                ),
                Column(
                  children: [
                    SizedBox(
                      child: Text('Não há nada aqui por enquanto pois isso é só um prototipo',
                      style: TextStyle(
                        fontSize: 25.0,
                        fontWeight: FontWeight.bold,
                      ),
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
