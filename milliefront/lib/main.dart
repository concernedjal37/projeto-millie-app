import 'package:flutter/material.dart';

void main() {
  //runApp(const MyApp());
  runApp(
    MaterialApp(
      home: Scaffold(
        appBar: AppBar(title: Text("data")),
        body: Text("Conteudo Principal"),
        bottomNavigationBar: BottomAppBar(
          child: Row(children: <Widget>[Text("Texto1")]),
        ),
      ),
    ),
  );
}

/*class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(theme: ThemeData(primaryColor: Colors.lightBlue));
  }
  //const MyApp({super.key});
}*/
