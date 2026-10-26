import 'package:flutter/material.dart';

class HomePage extends StatefulWidget {
  const HomePage({super.key});
  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<StatefulWidget> {
  @override
  Widget build(BuildContext context) {
    return Center(
      child: Container(
        color: Color.fromARGB(255, 25, 25, 80),
        width: double.infinity,
        child: Column(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Container(
              decoration: BoxDecoration(
                borderRadius: BorderRadius.vertical(top: Radius.zero, bottom: Radius.circular(10.0)),
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
    );
  }
}
