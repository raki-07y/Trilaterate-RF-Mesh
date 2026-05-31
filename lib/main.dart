import 'package:flutter/material.dart';
import 'screens/home_screen.dart';
import 'screens/map_screen.dart';
import 'screens/sos_screen.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'screens/auth_screen.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  
  // Initialize Supabase with actual keys
  await Supabase.initialize(
    url: 'https://hboporlyjwqdumwpymel.supabase.co',
    anonKey: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Imhib3Bvcmx5andxZHVtd3B5bWVsIiwicm9sZSI6ImFub24iLCJpYXQiOjE3ODAyMjI5MTMsImV4cCI6MjA5NTc5ODkxM30.gY2sZIiyMYIOUsMkPXNXYMcU5WH9Bg8gzc0fPX91x0Q',
  );

  runApp(const TouristGuardApp());
}

class TouristGuardApp extends StatelessWidget {
  const TouristGuardApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'TouristGuard',
      debugShowCheckedModeBanner: false,
      theme: ThemeData(
        useMaterial3: true,
        scaffoldBackgroundColor: const Color(0xFF0F172A), // Deep Slate
        colorScheme: const ColorScheme.dark(
          primary: Color(0xFF14B8A6), // Vibrant Teal Accent
          secondary: Color(0xFF38BDF8), // Light Blue
          surface: Color(0xFF1E293B),
          background: Color(0xFF0F172A),
          error: Color(0xFFF43F5E), // Rose Red for SOS
        ),
        textTheme: GoogleFonts.outfitTextTheme(
          ThemeData.dark().textTheme,
        ),
        appBarTheme: const AppBarTheme(
          backgroundColor: Colors.transparent,
          elevation: 0,
          centerTitle: true,
        ),
      ),
      initialRoute: Supabase.instance.client.auth.currentSession == null ? '/auth' : '/home',
      routes: {
        '/auth': (context) => const AuthScreen(),
        '/home': (context) => const HomeScreen(),
        '/map': (context) => const MapScreen(),
        '/sos': (context) => const SosScreen(),
      },
    );
  }
}
