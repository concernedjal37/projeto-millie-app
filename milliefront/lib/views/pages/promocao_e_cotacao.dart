import 'package:flutter/material.dart';

class PromocaoECotacao extends StatefulWidget {
  const PromocaoECotacao({super.key});
  @override
  // ignore: library_private_types_in_public_api
  _PromocaoECotacaoState createState() => _PromocaoECotacaoState();
}

class _PromocaoECotacaoState extends State<StatefulWidget> {
  String? menuItem = 'pro';
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
                    children: [
                      Padding(
                        padding: const EdgeInsets.all(5.0),
                        child: Column(
                          mainAxisAlignment: MainAxisAlignment.start,
                          crossAxisAlignment: CrossAxisAlignment.center,
                          children: [
                            SizedBox(
                              child: Image.asset(
                                'assets/images/Ilustracao414_3.png',
                                height: 200,
                                width: 450,
                              ),
                            ),
                            DropdownButton(
                              value: menuItem,
                              items: [
                                DropdownMenuItem(
                                  value: 'pro',
                                  child: Text('Promoções'),
                                ),
                                DropdownMenuItem(
                                  value: 'cot',
                                  child: Text('Cotações'),
                                ),
                              ],
                              onChanged: (String? value) {
                                setState(() {
                                  menuItem = value;
                                });
                              },
                            ),
                            TextField(
                              decoration: InputDecoration(
                                border: OutlineInputBorder(),
                                hintText: 'Pesquisar:',
                                hintStyle: TextStyle(
                                  color: Color(0xd0ffffff),
                                  fontSize: 18.0,
                                ),
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
                          padding: EdgeInsets.all(5.0),
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.start,
                            crossAxisAlignment: CrossAxisAlignment.center,
                            children: [
                              SizedBox(
                                child: Text(
                                  "Ultimas Pesquisas:",
                                  style: TextStyle(
                                    fontSize: 15,
                                    color: Colors.white,
                                  ),
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
