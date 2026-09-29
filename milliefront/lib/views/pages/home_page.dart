import 'package:flutter/material.dart';
import 'package:milliefront/views/pages/configuracoes.dart';
import 'package:milliefront/views/pages/historico_de_promocoes.dart';
import 'package:milliefront/views/pages/login.dart';
import 'package:milliefront/views/pages/perfil.dart';
import 'package:milliefront/views/pages/promocao_e_cotacao.dart';
import 'package:milliefront/views/pages/voos.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});
  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<StatefulWidget> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(),
      drawer: Drawer(
        child: Column(
          children: [
            DrawerHeader(child: Text('Millie')),
            ListTile(
              leading: Icon(Icons.login),
              title: Text('Login'),
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => Login()),
                );
              },
            ),
            ListTile(
              leading: Icon(Icons.person),
              title: Text('Perfil'),
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => Perfil()),
                );
              },
            ),
            ListTile(
              leading: Icon(Icons.settings),
              title: Text('Configurações'),
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => Configuracoes()),
                );
              },
            ),
          ],
        ),
      ),
      body: Center(
        child: Container(
          color: Color.fromARGB(255, 25, 25, 80),
          width: double.infinity,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Container(
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
                height: 200.0,
                width: double.infinity,
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Image.asset(
                      'assets/images/Ilustracao414_3.png',
                      height: 165,
                      width: 300,
                    ),
                    /* Padding(
                      padding: const EdgeInsets.all(5.0),
                      child: Row(
                        mainAxisAlignment: MainAxisAlignment.spaceAround,
                        mainAxisSize: MainAxisSize.max,
                        children: [
                          ElevatedButton(
                            onPressed: () {
                              Navigator.push(
                                context,
                                MaterialPageRoute(builder: (context) => Voos()),
                              );
                            },
                            child: Text("Voos"),
                          ),
                          ElevatedButton(
                            onPressed: () {
                              Navigator.push(
                                context,
                                MaterialPageRoute(
                                  builder: (context) => PromocaoECotacao(),
                                ),
                              );
                            },
                            child: Text("Promoções"),
                          ),
                          ElevatedButton(
                            onPressed: () {
                              Navigator.push(
                                context,
                                MaterialPageRoute(
                                  builder: (context) => PromocaoECotacao(),
                                ),
                              );
                            },
                            child: Text("Cotações"),
                          ),
                        ],
                      ),
                    ), */
                  ],
                ),
              ),
              Container(
                color: Color.fromARGB(255, 25, 25, 80),
                width: double.infinity,
                height: 300.0,
                child: ListView(
                  scrollDirection: Axis.horizontal,
                  reverse: false,
                  children: [
                    Card(
                      elevation: 3.0,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12.0),
                      ),
                      child: Container(
                        width: 200.0,
                        height: double.infinity,
                        decoration: BoxDecoration(
                          image: DecorationImage(
                            image: AssetImage('assets/images/promo1.jpg'),
                            fit: BoxFit.cover,
                          ),
                          gradient: LinearGradient(
                            colors: [
                              Color.fromARGB(255, 165, 165, 250),
                              Color.fromARGB(255, 30, 30, 250),
                            ],
                            begin: Alignment.topLeft,
                            end: Alignment.bottomRight,
                          ),
                        ),
                        padding: EdgeInsets.all(5.0),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              "Promoção 1",
                              style: TextStyle(
                                fontSize: 18.0,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            SizedBox(height: 8.0),
                            Text(
                              "Descrição da promoção 1.",
                              style: TextStyle(fontSize: 14.0),
                            ),
                          ],
                        ),
                      ),
                    ),
                    Card(
                      elevation: 3.0,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12.0),
                      ),
                      child: Container(
                        width: 200.0,
                        height: double.infinity,
                        decoration: BoxDecoration(
                          image: DecorationImage(
                            image: AssetImage('assets/images/promo2.jpg'),
                            fit: BoxFit.cover,
                          ),
                          gradient: LinearGradient(
                            colors: [
                              Color.fromARGB(255, 165, 165, 250),
                              Color.fromARGB(255, 30, 30, 250),
                            ],
                            begin: Alignment.topLeft,
                            end: Alignment.bottomRight,
                          ),
                        ),
                        padding: EdgeInsets.all(5.0),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              "Promoção 2",
                              style: TextStyle(
                                fontSize: 18.0,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            SizedBox(height: 8.0),
                            Text(
                              "Descrição da promoção 2.",
                              style: TextStyle(fontSize: 14.0),
                            ),
                          ],
                        ),
                      ),
                    ),
                    Card(
                      elevation: 3.0,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12.0),
                      ),
                      child: Container(
                        width: 200.0,
                        height: double.infinity,
                        decoration: BoxDecoration(
                          image: DecorationImage(
                            image: AssetImage('assets/images/promo3.jpg'),
                            fit: BoxFit.cover,
                          ),
                          gradient: LinearGradient(
                            colors: [
                              Color.fromARGB(255, 165, 165, 250),
                              Color.fromARGB(255, 30, 30, 250),
                            ],
                            begin: Alignment.topLeft,
                            end: Alignment.bottomRight,
                          ),
                        ),
                        padding: EdgeInsets.all(5.0),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              "Promoção 3",
                              style: TextStyle(
                                fontSize: 18.0,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            SizedBox(height: 8.0),
                            Text(
                              "Descrição da promoção 3.",
                              style: TextStyle(fontSize: 14.0),
                            ),
                          ],
                        ),
                      ),
                    ),
                    Card(
                      elevation: 3.0,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12.0),
                      ),
                      child: Container(
                        width: 200.0,
                        height: double.infinity,
                        decoration: BoxDecoration(
                          image: DecorationImage(
                            image: AssetImage('assets/images/promo4.jpg'),
                            fit: BoxFit.cover,
                          ),
                          gradient: LinearGradient(
                            colors: [
                              Color.fromARGB(255, 165, 165, 250),
                              Color.fromARGB(255, 30, 30, 250),
                            ],
                            begin: Alignment.topLeft,
                            end: Alignment.bottomRight,
                          ),
                        ),
                        padding: EdgeInsets.all(5.0),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              "Promoção 4",
                              style: TextStyle(
                                fontSize: 18.0,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            SizedBox(height: 8.0),
                            Text(
                              "Descrição da promoção 4.",
                              style: TextStyle(fontSize: 14.0),
                            ),
                          ],
                        ),
                      ),
                    ),
                    Card(
                      elevation: 3.0,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(12.0),
                      ),
                      child: Container(
                        width: 200.0,
                        height: double.infinity,
                        decoration: BoxDecoration(
                          image: DecorationImage(
                            image: AssetImage('assets/images/promo5.jpg'),
                            fit: BoxFit.cover,
                          ),
                          gradient: LinearGradient(
                            colors: [
                              Color.fromARGB(255, 165, 165, 250),
                              Color.fromARGB(255, 30, 30, 250),
                            ],
                            begin: Alignment.topLeft,
                            end: Alignment.bottomRight,
                          ),
                        ),
                        padding: EdgeInsets.all(5.0),
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              "Promoção 5",
                              style: TextStyle(
                                fontSize: 18.0,
                                fontWeight: FontWeight.bold,
                              ),
                            ),
                            SizedBox(height: 8.0),
                            Text(
                              "Descrição da promoção 5.",
                              style: TextStyle(fontSize: 14.0),
                            ),
                          ],
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
      bottomNavigationBar: NavigationBar(
        destinations: [
          NavigationDestination(
            icon: Icon(Icons.home),
            label: 'Home',
          ),
          NavigationDestination(
            icon: Icon(Icons.flight),
            label: 'Voos',
          ),
          NavigationDestination(
            icon: Icon(Icons.monetization_on),
            label: 'Promoções e Cotacões',
          ),
        ],
      ),
    );
  }
}
