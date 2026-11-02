import 'package:flutter/material.dart';

class Voos extends StatefulWidget {
  const Voos({super.key});
  @override
  // ignore: library_private_types_in_public_api
  _VoosState createState() => _VoosState();
}

class _VoosState extends State<StatefulWidget> {
  @override
  Widget build(BuildContext context) {
    return Center(
      child: Container(
        color: Color.fromARGB(255, 25, 25, 80),
        width: double.infinity,
        child: Column(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Flexible(
              child: Padding(
                padding: const EdgeInsets.all(10.0),
                child: Container(
                  decoration: BoxDecoration(
                    borderRadius: BorderRadius.circular(10.0),
                    gradient: LinearGradient(
                      colors: [
                        Color.fromARGB(255, 165, 165, 250),
                        Color.fromARGB(255, 30, 30, 250),
                      ],
                      begin: Alignment.topLeft,
                      end: Alignment.bottomRight,
                    ),
                  ),
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.start,
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Container(
                        padding: EdgeInsets.all(10.0),
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.start,
                          crossAxisAlignment: CrossAxisAlignment.center,
                          children: [
                            SizedBox(
                              child: Text(
                                "Ida",
                                style: TextStyle(
                                  fontSize: 30,
                                  color: Colors.white,
                                ),
                              ),
                            ),
                            TextField(
                              decoration: InputDecoration(
                                border: OutlineInputBorder(),
                                hintText: 'Local de partida:',
                                hintStyle: TextStyle(
                                  color: Color(0xd0ffffff),
                                  fontSize: 18.0,
                                ),
                              ),
                            ),
                            TextField(
                              decoration: InputDecoration(
                                border: OutlineInputBorder(),
                                hintText: 'Local do destino:',
                                hintStyle: TextStyle(
                                  color: Color(0xd0ffffff),
                                  fontSize: 18.0,
                                ),
                              ),
                            ),
                            SizedBox(
                              child: Text(
                                "Volta",
                                style: TextStyle(
                                  fontSize: 30,
                                  color: Colors.white,
                                ),
                              ),
                            ),
                            TextField(
                              decoration: InputDecoration(
                                border: OutlineInputBorder(),
                                hintText: 'Local de partida:',
                                hintStyle: TextStyle(
                                  color: Color(0xd0ffffff),
                                  fontSize: 18.0,
                                ),
                              ),
                            ),
                            TextField(
                              decoration: InputDecoration(
                                border: OutlineInputBorder(),
                                hintText: 'Local do destino:',
                                hintStyle: TextStyle(
                                  color: Color(0xd0ffffff),
                                  fontSize: 18.0,
                                ),
                              ),
                            ),
                            Container(
                              padding: EdgeInsets.all(5.0),
                              child: Row(
                                mainAxisAlignment:
                                    MainAxisAlignment.spaceEvenly,
                                children: [
                                  ElevatedButton(
                                    onPressed: () {},
                                    child: Text("Filtro"),
                                  ),
                                  ElevatedButton(
                                    onPressed: () {},
                                    child: Text("Confirmar"),
                                  ),
                                ],
                              ),
                            ),
                          ],
                        ),
                      ),
                      Flexible(
                        child: Container(
                          decoration: BoxDecoration(
                            borderRadius: BorderRadius.vertical(top: Radius.zero, bottom: Radius.circular(10.0)),
                            color: Color(0xff303070),
                          ),
                          width: double.infinity,
                          child: ListView(
                            padding: EdgeInsets.all(5.0),
                            scrollDirection: Axis.vertical,
                            children: [
                              Card(
                                elevation: 5,
                                child: ListTile(
                                  title: Text("Voo 1"),
                                  subtitle: Text("Detalhes do voo 1"),
                                ),
                              ),
                              Card(
                                elevation: 5,
                                child: ListTile(
                                  title: Text("Voo 2"),
                                  subtitle: Text("Detalhes do voo 2"),
                                ),
                              ),
                              Card(
                                elevation: 5,
                                child: ListTile(
                                  title: Text("Voo 3"),
                                  subtitle: Text("Detalhes do voo 3"),
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
