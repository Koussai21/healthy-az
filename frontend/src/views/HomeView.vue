<script setup>
import { RouterLink } from "vue-router";
import PixelCardiometer from "../components/PixelCardiometer.vue";
</script>

<template>
  <section class="hero">
    <div class="hero-copy">
      <p class="eyebrow">Encyclopédie collaborative de la santé</p>
      <h1 class="h1">Healthy-AZ réunit maladies, symptômes et diagnostics.</h1>
      <p class="lead muted">
        Recherchez comme sur un moteur classique, explorez des fiches claires, échangez sur le forum et
        discutez en privé — avec un assistant IA local (Phi‑3 via Ollama) pour des repères généraux, sans
        remplacer un professionnel.
      </p>
      <div class="cta">
        <RouterLink class="btn" to="/encyclopedie">Ouvrir l'encyclopédie</RouterLink>
        <RouterLink class="btn btn-ghost" to="/inscription">Créer un compte</RouterLink>
      </div>
    </div>
    <PixelCardiometer />
  </section>

  <section class="grid card features">
    <div>
      <h2 class="h2">Recherche naturelle</h2>
      <p class="muted">
        Tapez une phrase ou des mots-clés : les titres, résumés et contenus sont parcourus pour afficher les
        fiches les plus pertinentes.
      </p>
    </div>
    <div>
      <h2 class="h2">Trois types de fiches</h2>
      <p class="muted">Maladies, symptômes et diagnostics — chacune avec sa page dédiée et une URL stable.</p>
    </div>
    <div>
      <h2 class="h2">Communauté</h2>
      <p class="muted">Forum public, messagerie entre membres et contribution de nouvelles entrées après connexion.</p>
    </div>
  </section>
</template>

<style scoped>
.hero {
  display: grid;
  gap: 1.75rem;
  align-items: center;
}

@media (min-width: 900px) {
  .hero {
    grid-template-columns: 1fr 1.05fr;
  }
}

.eyebrow {
  text-transform: uppercase;
  letter-spacing: 0.12em;
  font-size: 0.72rem;
  color: var(--accent);
  margin: 0 0 0.5rem;
  font-weight: 600;
}

.lead {
  font-size: 1.05rem;
  line-height: 1.55;
  margin: 0 0 1.25rem;
}

.cta {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.features {
  margin-top: 0.5rem;
  display: grid;
  gap: 1.25rem;
}

@media (min-width: 720px) {
  .features {
    grid-template-columns: repeat(3, 1fr);
  }
}

.features .h2 {
  font-size: 1.1rem;
}
</style>
