import 'package:flutter/material.dart';
import 'package:milliefront/views/pages/home_page.dart';

class PromocaoECotacao extends StatefulWidget {
  const PromocaoECotacao({super.key});
  @override
  // ignore: library_private_types_in_public_api
  _PromocaoECotacaoState createState() => _PromocaoECotacaoState();
}
class _PromocaoECotacaoState extends State<StatefulWidget> {
  @override
  Widget build(BuildContext context){
    return Scaffold(
      body: Center(
        child: Container(
          color: Color.fromARGB(255, 25, 25, 80),
          width: double.infinity,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Flexible(
                child: Container(
                  color: Color.fromARGB(255, 50, 50, 240),
                  child: Column(
                    children: [
                      ElevatedButton(onPressed: () {
                        Navigator.push(context, MaterialPageRoute(builder: (context) => HomePage()));
                      },
                      child: Text("Home")),
                      Column(
                        mainAxisAlignment: MainAxisAlignment.start,
                        crossAxisAlignment: CrossAxisAlignment.center,
                        children: [
                          SizedBox(
                            child: Image.asset('assets/images/Ilustracao414_3.png',
                              height: 200,
                              width: 450,
                            ),
                          ),
                          SizedBox(
                            child: Text("Pesquisar",
                              style: TextStyle(
                                fontSize: 30,
                                color: Colors.white,
                              ),
                            ),
                          ),
                          TextField(
                            decoration: InputDecoration(border: OutlineInputBorder()),
                          ),
                        ],
                      ),
                      Flexible(
                        child: Container(
                          color: Color(0xff303070),
                          width: double.infinity,
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.start,
                            crossAxisAlignment: CrossAxisAlignment.center,
                            children: [
                              SizedBox(
                                child: Text("Ultimas Pesquisas:",
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
            ],
          ),
        ),
      ),
    );
  }
}