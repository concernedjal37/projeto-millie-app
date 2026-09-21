import 'package:flutter/material.dart';
import 'package:milliefront/views/pages/home_page.dart';

class HistoricoDePromocoes extends StatefulWidget {
  const HistoricoDePromocoes({super.key});
  @override
  _HistoricoDePromocoesState createState() => _HistoricoDePromocoesState();
}

class _HistoricoDePromocoesState extends State<StatefulWidget> {
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
                
              ],
            ),
          ),
        ),
      ),
    );
  }
}
