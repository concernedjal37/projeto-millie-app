import 'package:flutter/material.dart';
import 'package:milliefront/data/notifiers.dart';

class NavbarWidget extends StatelessWidget {
  const new({super.key});

  @override
  Widget build(BuildContext context) {
    return ValueListenableBuilder(
      valueListenable: selectedPageNotifier,
      builder: (context, selectedPage, child) {
        return NavigationBar(
          destinations: [
            NavigationDestination(icon: Icon(Icons.home), label: 'Home'),
            NavigationDestination(icon: Icon(Icons.flight), label: 'Voos'),
            NavigationDestination(
              icon: Icon(Icons.monetization_on),
              label: 'Promoções e Cotações',
            ),
          ],
          onDestinationSelected: (int value) {
            selectedPageNotifier.value = value;
          },
          selectedIndex: selectedPage,
        );
      },
    );
  }
}
