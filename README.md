# 🌸 NALA: De los Leus al Euro  
### _Un análisis exploratorio de precios y accesibilidad en dos economías europeas_  
### Presentacion en Power Point y Streamlit (app.py)

---

## 🧴 Sobre NALA  

**Nala** es una marca de **cosmética natural, artesanal y vegana** que ofrece productos para el cuidado del cuerpo, manos, pies, cabello y baño.  
Sus fórmulas destacan por ser **naturales, ecológicas, sostenibles y libres de crueldad animal**, con una amplia variedad de aromas y texturas 🌿✨.  

---

## 🗺️ Contexto del Proyecto  

Este análisis estudia la estrategia de precios y accesibilidad de **Nala** en dos mercados europeos con distintas realidades económicas: **España** y **Rumanía**.  

| País | Moneda | Portal | Productos |
|------|---------|---------|-----------|
| 🇪🇸 España | Euro (€) | [nala.es](https://nala.es) | 381 |
| 🇷🇴 Rumanía | Leu (LEI) | [nala.ro](https://nala.ro) | 342 |
| **Total** |  |  | **723 productos** |

**Objetivo:**  
Evaluar cómo varían los precios y la accesibilidad de los productos de Nala según el contexto económico local.  

**Pregunta Clave:**  
> ¿Es Nala igual de accesible en España y Rumanía considerando el poder adquisitivo local?

---

## 🧠 Hipótesis  

1. **Accesibilidad:** Los precios en Rumanía son menos accesibles considerando el salario mínimo.  
2. **Estructura de precios:** Existen diferencias en el mix de productos y posicionamiento por gama.  

---

## ⚙️ Metodología  

1. **Obtención de datos:**  
   - Webscraping desde los portales oficiales (`nala.es` y `nala.ro`).  
   - Total: **723 productos únicos.**  

2. **Limpieza y normalización:**  
   - Se eliminaron packs y sets.  
   - Se excluyó la categoría “Otro”.  
   - Se normalizaron formatos y monedas.  

3. **Análisis Exploratorio:**  
   - Histogramas y boxplots comparativos por país.  
   - Análisis de categorías generales y específicas.  
   - Cálculo de accesibilidad considerando el salario mínimo de cada país.  

---

## 📊 Resultados Clave  

### 💶 Distribución General de Precios  

- **España:** precios más concentrados entre **€4.9 y €9.9**.  
- **Rumanía:** mayor dispersión, con precios entre **19.9 y 53.4 LEI** (≈ €4–€11).  
- **Insight:** Rumanía presenta un mercado más variable, con mezcla de productos económicos y premium.  

---

### 🧴 Comparativa por Categoría  

| Categoría | España (€) | Rumanía (€ convertido) |
|------------|-------------|------------------------|
| Rostro | 10.09 | 8.82 |
| Corporal | 9.50 | 8.00 |
| Cabello | 8.97 | 7.07 |
| Ducha y Baño | 5.50 | 4.90 |

📍 *Conclusión:* España mantiene precios ligeramente más altos, reflejando un **posicionamiento más premium**.  
Rumanía, por su parte, se ajusta a un mercado más competitivo.  

---

### 🪞 Productos Destacados  

- 💎 **Más caros:** Sérum Facial Premium y Crema Reafirmante — ambos más costosos en Rumanía.  
- 🍃 **Más económicos:** Jabón Natural y Crema de Baño — más baratos en Rumanía.  

💬 *El mismo producto puede tener diferencias de precio notables entre ambos países debido a la estrategia de posicionamiento y al cambio de moneda.*  

---

### 📈 Accesibilidad Económica  

- Costo promedio de un producto ≈ **0.7 % del salario mínimo**.  
- Con un salario mínimo mensual se pueden adquirir:  
  - 🇪🇸 **≈150 productos** en España  
  - 🇷🇴 **≈135 productos** en Rumanía  

📊 *España resulta un poco más accesible, aunque la diferencia es leve en términos de poder adquisitivo real.*  

---

## 💡 Insights Finales  

1. **Mercado español:** precios más homogéneos y estables.  
2. **Mercado rumano:** mayor variabilidad de precios y mezcla de gamas.  
3. **Accesibilidad:** prácticamente igual en ambos países.  
4. **Rumanía** ofrece precios más competitivos en básicos, pero más altos en productos especializados.  

---

## ✅ Conclusiones  

- **Hipótesis principal (accesibilidad):** ❌ No se cumple.  
  > Los precios son ligeramente más altos en España, pero ambos países mantienen **niveles de accesibilidad similares**.  

- **Hipótesis secundaria (estructura de precios):** ⚠️ Se cumple parcialmente.  
  > Ambos países concentran su oferta en la gama media, aunque **Rumanía muestra una mayor dispersión** de precios.  

> _“La belleza natural no entiende de fronteras, pero la economía sí.”_  

---

## 🧰 Herramientas Utilizadas  

| Etapa | Tecnologías |
|-------|--------------|
| Extracción | `Python`, `BeautifulSoup`, `Selenium` |
| Limpieza y análisis | `Pandas`, `NumPy`, `Matplotlib`, `Seaborn` |
| Documentación | `Jupyter Notebook`, `PowerPoint`, `Markdown` |

---

## 🌍 Reflexión Final  

El análisis de Nala entre España y Rumanía demuestra que, aunque los precios pueden parecer distintos, el **valor percibido y la accesibilidad real** se mantienen cercanos.  
Este estudio evidencia cómo **el análisis de datos** permite entender mejor las dinámicas económicas internacionales y adaptar estrategias de marca sostenible sin perder coherencia.  

---

## 👩‍💻 Autora  

**Rosinela Vega**  
🎓 *Proyecto: De los Leus al Euro – Análisis Exploratorio de Datos*  
💼 *Marca: Nala Cosmetics*  


---



