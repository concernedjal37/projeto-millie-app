import 'package:flutter/material.dart';
import 'package:milliefront/views/pages/home_page.dart';

class Login extends StatefulWidget {
  const Login({super.key});
  @override
  // ignore: library_private_types_in_public_api
  _LoginState createState() => _LoginState();
}
class _LoginState extends State<StatefulWidget> {
  var _nomeUsuario = "";
  var _senha = "";
  @override
  Widget build(BuildContext context){
    return Scaffold(
      body: Center(
        child: Container(
          color: Color.fromARGB(255, 30, 30, 130),
          padding: EdgeInsets.all(50.0),
          child: Container(
            padding: EdgeInsets.all(10.0),
            decoration: BoxDecoration(
              color: Color(0xffffffff),
              borderRadius: BorderRadius.circular(25.0),
            ),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                SizedBox(
                  child: Image.asset('assets/images/Logo_preto.png',
                    height: 200,
                    width: 450,
                  ),
                ),
                SizedBox(
                  child: Text("Usuario",
                    style: TextStyle(
                      fontSize: 30,
                      color: Colors.black,
                    ),
                  ),
                ),
                TextField(
                  decoration: InputDecoration(border: OutlineInputBorder()),
                ),
                SizedBox(
                  child: Text("Senha",
                    style: TextStyle(
                      fontSize: 30,
                      color: Colors.black,
                    ),
                  ),
                ),
                TextField(
                  decoration: InputDecoration(border: OutlineInputBorder()),
                ),
                ElevatedButton(onPressed: () {
                  Navigator.push(context, MaterialPageRoute(builder: (context) => HomePage()));
                },
                style: ElevatedButton.styleFrom(
                  backgroundColor: Color.fromARGB(255, 95, 95, 207),
                ),
                child: Text("Entrar",
                style: TextStyle(
                  color: Colors.white,
                ),
                )),
                TextButton(onPressed: () {
                  
                },
                child: Text("Esqueci Minha senha",
                style: TextStyle(
                  fontSize: 10,
                  color: Colors.blueAccent,
                ),
                )),
              ],
            ),
          ),
        ),
      ),
    );
  }
}