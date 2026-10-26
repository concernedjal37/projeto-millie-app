import 'package:flutter/material.dart';

class NavbarWidget extends StatefulWidget {
  const new({super.key});

  @override
  State<NavbarWidget> createState() => _NavbarWidgetState();
}

class _NavbarWidgetState extends State<NavbarWidget> {
  int selectedIndex = 0;
  @override
  Widget build(BuildContext context) {
    return NavigationBar(
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
            label: 'Promoções e Cotações',
          ),
        ],
        onDestinationSelected: (int value) {
          setState(() {
            selectedIndex = value;
          });
        },
        selectedIndex: selectedIndex,
      );
  }
}