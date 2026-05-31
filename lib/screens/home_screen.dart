import 'package:flutter/material.dart';
import '../widgets/glass_card.dart';
import '../services/supabase_service.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      extendBodyBehindAppBar: true,
      appBar: AppBar(
        title: const Text('TouristGuard', style: TextStyle(fontWeight: FontWeight.bold)),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () async {
              await SupabaseService().signOut();
              if (context.mounted) {
                Navigator.pushReplacementNamed(context, '/auth');
              }
            },
          )
        ],
      ),
      body: Stack(
        children: [
          // Dynamic Background Gradients
          Container(
            decoration: const BoxDecoration(
              gradient: LinearGradient(
                begin: Alignment.topLeft,
                end: Alignment.bottomRight,
                colors: [Color(0xFF0F172A), Color(0xFF1E293B), Color(0xFF0F172A)],
              ),
            ),
          ),
          Positioned(
            top: -100,
            left: -50,
            child: Container(
              width: 300,
              height: 300,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: Theme.of(context).colorScheme.primary.withOpacity(0.15),
              ),
            ),
          ),
          SafeArea(
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 20.0),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  const SizedBox(height: 20),
                  const Text(
                    'Welcome to Paris',
                    style: TextStyle(fontSize: 16, color: Colors.white70),
                  ),
                  const Text(
                    'Stay Safe Today',
                    style: TextStyle(fontSize: 32, fontWeight: FontWeight.bold, color: Colors.white),
                  ),
                  const SizedBox(height: 30),
                  
                  // Safety Score Glass Card
                  GlassCard(
                    padding: const EdgeInsets.all(24),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            const Text(
                              'Safety Score',
                              style: TextStyle(fontSize: 18, color: Colors.white70),
                            ),
                            const SizedBox(height: 8),
                            Text(
                              '98/100',
                              style: TextStyle(
                                fontSize: 40, 
                                fontWeight: FontWeight.bold, 
                                color: Theme.of(context).colorScheme.primary
                              ),
                            ),
                          ],
                        ),
                        Container(
                          padding: const EdgeInsets.all(12),
                          decoration: BoxDecoration(
                            color: Theme.of(context).colorScheme.primary.withOpacity(0.2),
                            shape: BoxShape.circle,
                          ),
                          child: Icon(Icons.shield_outlined, 
                            size: 40, 
                            color: Theme.of(context).colorScheme.primary
                          ),
                        )
                      ],
                    ),
                  ),
                  
                  const SizedBox(height: 30),
                  const Text(
                    'Quick Actions',
                    style: TextStyle(fontSize: 20, fontWeight: FontWeight.w600, color: Colors.white),
                  ),
                  const SizedBox(height: 16),
                  
                  // Action Grid
                  Expanded(
                    child: GridView.count(
                      crossAxisCount: 2,
                      crossAxisSpacing: 16,
                      mainAxisSpacing: 16,
                      children: [
                        _buildActionCard(
                          context,
                          'Safe Routes',
                          Icons.map_outlined,
                          Theme.of(context).colorScheme.primary,
                          () => Navigator.pushNamed(context, '/map'),
                        ),
                        _buildActionCard(
                          context,
                          'Emergency SOS',
                          Icons.warning_amber_rounded,
                          Theme.of(context).colorScheme.error,
                          () => Navigator.pushNamed(context, '/sos'),
                        ),
                        _buildActionCard(
                          context,
                          'Nearby Help',
                          Icons.local_hospital_outlined,
                          Theme.of(context).colorScheme.secondary,
                          () {},
                        ),
                        _buildActionCard(
                          context,
                          'Alerts',
                          Icons.notifications_active_outlined,
                          Colors.amber,
                          () {},
                        ),
                      ],
                    ),
                  ),
                ],
              ),
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildActionCard(BuildContext context, String title, IconData icon, Color color, VoidCallback onTap) {
    return GlassCard(
      onTap: onTap,
      padding: const EdgeInsets.all(16),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(icon, size: 48, color: color),
          const SizedBox(height: 12),
          Text(
            title,
            textAlign: TextAlign.center,
            style: const TextStyle(fontSize: 16, fontWeight: FontWeight.w500, color: Colors.white),
          ),
        ],
      ),
    );
  }
}
