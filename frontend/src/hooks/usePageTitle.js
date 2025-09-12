import { useEffect } from 'react';

export function usePageTitle(title, icon = null) {
  useEffect(() => {
    // Atualizar o título da página
    document.title = title;
    
    // Atualizar o favicon se fornecido
    if (icon) {
      const link = document.querySelector("link[rel*='icon']") || document.createElement('link');
      link.type = 'image/svg+xml';
      link.rel = 'shortcut icon';
      link.href = icon;
      
      document.getElementsByTagName('head')[0].appendChild(link);
    }
  }, [title, icon]);
}
