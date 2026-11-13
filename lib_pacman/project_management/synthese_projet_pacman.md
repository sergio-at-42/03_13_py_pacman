# PAC-MAN — Synthèse du projet et bilan de réalisation

## 1. Présentation du projet

Le projet **PAC-MAN** a été réalisé par **Sana Saidi** et **Serge Beldjaoui** sur une période de **trois semaines de travail effectif**, hors week-ends.

L’objectif était de concevoir un jeu Pac-Man fonctionnel, structuré en plusieurs modules et accompagné de ses interfaces, de ses fonctionnalités de jeu, de ses tests et de sa documentation.

Le travail a été organisé progressivement : cadrage et architecture, développement des fonctionnalités principales, intégration, puis vérification et préparation des livrables.

## 2. Organisation et répartition du travail

La répartition des tâches a permis à chacun de contribuer à plusieurs aspects du projet. Elle n’a pas été cloisonnée : **les deux membres ont participé à la fois au développement du jeu et à la conception de l’interface utilisateur**.

Les responsabilités principales ont été réparties de la manière suivante :

- **Serge** : développement du parseur et de la configuration, logique du joueur et des fantômes, fonctionnalités du moteur de jeu et plusieurs écrans.
- **Sana** : gestion et suivi du projet, génération du labyrinthe, placement des pac-gommes, rendu initial avec Pygame, interface du menu, orchestration des différentes parties avec la classe `Session` et préparation de la documentation.
- **Travail commun** : définition de l’architecture, organisation des fichiers, intégration des modules, tests d’affichage et tests croisés avant les revues.

Cette organisation a favorisé le partage des connaissances et une bonne compréhension de l’ensemble du projet par les deux membres.

## 3. Déroulement du projet

### Semaine 1 — Cadrage, architecture et premières fonctionnalités

**Serge**
- Développement du parseur de configuration.
- Gestion du fichier de configuration et de ses paramètres.

**Sana**
- Gestion du projet : préparation du diagramme de Gantt et suivi de l’avancement des tâches.
- Génération du labyrinthe et réalisation des tests associés.
- Placement des pac-gommes et des super-pac-gommes.
- Mise en place du rendu de base avec Pygame.

**Travail commun**
- Définition de l’architecture du projet.
- Organisation des modules, des classes et des fichiers.
- Mise en commun des premières parties développées.

**Résultat de la semaine :** les bases techniques du projet ont été mises en place : structure du code, configuration, génération du labyrinthe et premier affichage du jeu.

### Semaine 2 — Développement du gameplay et de l’interface

**Serge**
- Développement des fantômes :
  - poursuite du joueur avec l’algorithme BFS ;
  - comportement de fuite ;
  - état comestible ;
  - réapparition dans un coin du labyrinthe.
- Développement du joueur :
  - déplacements et collisions ;
  - gestion des vies et réapparition ;
  - gestion du score, des pac-gommes et des super-pac-gommes.
- Affichage des informations de jeu et mise en place de l’écran de pause.

**Sana**
- Développement de l’interface utilisateur :
  - affichage du menu principal ;
  - création de la classe `Session` pour relier les différentes parties du jeu et gérer les transitions entre les écrans.

**Travail commun**
- Tests des fonctionnalités d’affichage.
- Intégration et mise en commun des développements.
- Vérification du fonctionnement des différentes parties après leur assemblage.

**Résultat de la semaine :** les principales mécaniques de jeu ont été développées et l’interface a commencé à relier les différents éléments dans une expérience cohérente.

### Semaine 3 — Finalisation, robustesse et livrables

**Serge**
- Réalisation de tests sur le module de configuration et le moteur de jeu.
- Développement ou finalisation des écrans de highscores, de fin de partie (*Game Over*) et de victoire.

**Sana**
- Préparation des livrables de gestion de projet.
- Finalisation du README et de la documentation associée.

**Travail commun**
- Réalisation de tests avant les revues.
- Tests croisés du code et vérification de l’intégration.
- Correction des anomalies détectées et dernières vérifications.

**Résultat de la semaine :** les fonctionnalités ont été finalisées, les principaux contrôles ont été effectués et les éléments nécessaires à la livraison ont été préparés.

## 4. Communication et collaboration

La communication entre les deux membres a joué un rôle important dans l’avancement du projet. Les échanges réguliers ont facilité la coordination, la compréhension des interfaces entre les modules et la résolution des difficultés rencontrées.

La répartition des tâches a été équilibrée tout en restant suffisamment souple pour permettre à chacun d’intervenir sur différentes parties du projet. Le fait que les deux membres aient travaillé sur le jeu et sur l’interface utilisateur a également facilité l’intégration et la cohérence de l’ensemble.

La mise en commun régulière du travail a permis de repérer plus tôt les problèmes d’intégration et d’éviter de découvrir toutes les incompatibilités à la fin du développement.

## 5. Tests et vérification

Les tests ont accompagné le développement tout au long du projet. Ils ont notamment permis de vérifier les modules séparément, puis leur comportement une fois intégrés.

Les vérifications ont porté, entre autres, sur :
- la génération du labyrinthe et le placement des éléments ;
- les comportements du joueur et des fantômes ;
- la configuration et le moteur de jeu ;
- l’affichage et les transitions entre les écrans ;
- le fonctionnement global du jeu après intégration.

Les tests croisés, réalisés avant les revues, ont été particulièrement utiles : chacun a pu examiner le travail de l’autre, détecter des problèmes et contribuer à leur correction.

**Les tests ont ainsi joué un rôle préventif**, en permettant d’identifier certaines anomalies avant qu’elles ne deviennent des problèmes plus importants lors de l’intégration finale.

## 6. Bilan du projet

Le projet a été réalisé sur trois semaines de travail effectif, avec une progression organisée en trois grandes étapes : mise en place des fondations, développement des fonctionnalités, puis finalisation et vérification.

Les principaux points positifs de cette réalisation sont :
- une répartition des tâches claire, mais non cloisonnée ;
- une contribution des deux membres au gameplay comme à l’interface ;
- une communication efficace tout au long du développement ;
- une intégration progressive des modules ;
- des tests réguliers qui ont permis de prévenir et de corriger des problèmes ;
- un suivi de l’avancement grâce au diagramme de Gantt.

Cette expérience a permis de mener le projet collectivement, en combinant développement technique, conception de l’interface, organisation et vérification du travail réalisé.

---

*Document de synthèse du projet PAC-MAN — Sana Saidi et Serge Beldjaoui.*
