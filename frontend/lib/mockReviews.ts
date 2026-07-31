export const getMockReviewsForTopic = (topic: string) => {
  return [
    { source: 'Reddit', text: `I tried using ${topic} but the onboarding was incredibly confusing. It took me 2 hours just to figure out how to set it up.` },
    { source: 'Quora', text: `Is ${topic} a scam? Their pricing page is very deceptive and hidden fees showed up at checkout.` },
    { source: 'Google Reviews', text: `Customer support for ${topic} is non-existent. I opened a ticket 6 days ago and still no resolution.` },
    { source: 'MouthShut', text: `The mobile app for ${topic} crashes every time I try to complete an action. Unusable.` },
    { source: 'Twitter / X', text: `Why does the paid plan for ${topic} jump 10x in price? The free plan is way too limited.` },
    { source: 'Reddit', text: `Integrations with ${topic} don't work half the time. Very unreliable and frustrating.` },
    { source: 'Google Reviews', text: `The dashboard for ${topic} is overwhelming on first use. Too many options with no guidance.` },
    { source: 'Justdial', text: `Would love a dark mode for ${topic}. It would make daily use much nicer.` },
    { source: 'Reddit', text: `I signed up for ${topic} three times and still don't know what the product actually does. Terrible UX.` },
    { source: 'Twitter / X', text: `Auto-reply said 24-48 hours for ${topic} support. It's been a week and nothing.` },
  ];
};
