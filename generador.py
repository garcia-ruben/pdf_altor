from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import os
from io import BytesIO
import matplotlib.pyplot as plt

def fn_generar_graficas_svg(datos):
   # --- Gráfica de pastel ---
   etiquetas = [
      "En directo",
      "En Reporto",
      "Mercado de Capitales",
      "Saldo efectivo"
   ]
   valores = [
      0.00,
      1342717.84,
      0.00,
      94.32
   ]
   colores = [
      "#0291A4",
      "#005A7A",
      "#C2C2C2",
      "#D7E2E4"
   ]

   figura_pastel, eje_pastel = plt.subplots(figsize = (4, 3.3))
   segmentos, textos, porcentajes = eje_pastel.pie(
      valores,
      labels = None,
      colors = colores,
      autopct = lambda p: f"{p:.2f}%",
      startangle = 0,
      textprops = {
         "fontsize": 10,
         "fontweight": "bold"
      },
      pctdistance = 0.6,
      wedgeprops = {
         "edgecolor": "#005A7A",
         "linewidth": 0
      }
   )
   eje_pastel.axis("equal")
   eje_pastel.legend(
      segmentos,
      etiquetas,
      loc = "center left",
      bbox_to_anchor= (1, 0.5),
      fontsize = 10
   )

   buffer_svg_pastel = BytesIO()
   figura_pastel.savefig(
      buffer_svg_pastel,
      format = "svg",
      bbox_inches = "tight"
   )
   plt.close(figura_pastel)
   grafica_pastel_svg = buffer_svg_pastel.getvalue().decode("utf-8")

   # --- Gráfica de línea ---
   meses = [
      "ENE", "FEB", "MAR",
      "ABR", "MAY", "JUN",
      "JUL", "AGO", "SEP",
      "OCT", "NOV", "DIC"
   ]
   valores_cartera = [
      1230000, 1240000, 1250000, 1260000,
      1270000, 1280000, 1290000, 1300000,
      1310000, 1320000, 1330000, 1340000
   ]

   figura_linea, eje_linea = plt.subplots(figsize = (5, 3))

   eje_linea.plot(
      meses,
      valores_cartera,
      color = "#3E8EF1",
      linewidth = 3
   )
   eje_linea.ticklabel_format(axis = "y", style = "plain")
   eje_linea.set_title("")
   eje_linea.text(
      x = -0.13,
      y = 1.10,
      s = "Valor de la Cartera al final del periodo",
      fontsize = 14,
      fontweight = "bold",
      transform = eje_linea.transAxes,
      ha = "left",
      va = "bottom"
   )
   eje_linea.set_ylim(0, max(valores_cartera) + 100000)
   eje_linea.spines["top"].set_visible(False)
   eje_linea.spines["bottom"].set_visible(False)
   eje_linea.tick_params(axis = "x", labelrotation = 0)
   eje_linea.tick_params(axis = "both", labelsize = 8)

   eje_linea.xaxis.set_tick_params(pad = 20)
   eje_linea.yaxis.grid(
      True,
      linestyle = "-",
      alpha = 0.5
   )

   buffer_svg_linea = BytesIO()
   figura_linea.savefig(
      buffer_svg_linea,
      format = "svg",
      bbox_inches = "tight"
   )
   plt.close(figura_linea)
   grafica_linea_svg = buffer_svg_linea.getvalue().decode("utf-8")

   return {
      "grafica_pastel_svg": grafica_pastel_svg or "",
      "grafica_linea_svg": grafica_linea_svg or ""
   }

   return

def fn_generar_pdf(paginas, indice):
   datos = {
      "nombre_cliente": "AUTO BLITZ",
      "num_cliente_contrato": "C00031",
      "moneda": "MXN",
      "rfc": "XAXX010101000",
      "regimen_fiscal": "Regimen fiscal de personas morales",
      "paginas": paginas
   }

   env = Environment(loader = FileSystemLoader("templates"))
   plantilla = env.get_template("base.html")
   html = plantilla.render(**datos)

   ruta_pdf = os.path.join("pdf", f"salida_{indice}.pdf")
   os.makedirs(os.path.dirname(ruta_pdf), exist_ok = True)

   HTML(
      string = html,
      base_url = "."
   ).write_pdf(ruta_pdf)

   print(f"PDF guardado en: {os.path.abspath(ruta_pdf)}")

def fn_crear_tabla_resumen():
   datos = {
      "rfc_cliente": "XAXX010101000",
      "direccion": "CARR VHSA A NACAJUCA KM 14",
      "colonia": "ARROYO",
      "municipio": "NACAJUCA",
      "codigo_postal": "86243",
      "clave_regimen_fiscal": "601",
      "ejecutivo": "GREGORIO ARREOLA NABOR",
      "periodo": "01 al 31 de julio de 2025",
      "fecha_corte": "31/07/2025",
      "dias_periodo": "31",
      "tipo_envio": "Correo electrónico",
      "resumen_cartera_inversion": [
         {
            "nombre": "Mercado de Dinero En directo",
            "anterior": "$0.00",
            "total_anterior": "0.00%",
            "actual": "$0.00",
            "total_actual": "0.00%",
            "variacion": "0.00%",
         },
         {
            "nombre": "En Reporto",
            "anterior": "$1,332,837.33",
            "total_anterior": "100.00%",
            "actual": "$1,342,717.84",
            "total_actual": "99.99%",
            "variacion": "0.74%",
         },
         {
            "nombre": "Mercado de Capitales",
            "anterior": "$0.00",
            "total_anterior": "0.00%",
            "actual": "$0.00",
            "total_actual": "0.00%",
            "variacion": "0.00%",
         },
         {
            "nombre": "Saldo efectivo",
            "anterior": "$0.86",
            "total_anterior": "0.00%",
            "actual": "$94.32",
            "total_actual": "0.01%",
            "variacion": "10,867.44%",
         },
         {
            "nombre": "Totales",
            "anterior": "$1,332,838.19",
            "total_anterior": "100.00%",
            "actual": "$1,342,812.16",
            "total_actual": "100.00%",
            "variacion": "0.75%",
         }
      ],
      "operaciones_pendientes": [
         {
            "nombre": "Mercado de Dinero en directo",
            "compras": "0.00",
            "ventas": "0.00"
         },
         {
            "nombre": "Mercado de Capitales",
            "compras": "0,00",
            "ventas": "0.00"
         }
      ],
      "rendimientos": [
         {
            "nombre": "Mercado de Dinero en directo",
            "cantidad": "10,558.60",
            "porcentaje": "0.79"
         },
         {
            "nombre": "Mercado de Capitales",
            "cantidad": "9,973.97",
            "porcentaje": "0.74"
         }
      ],
      "resumen_movimientos": [
         {
            "nombre": "Saldo Anterior",
            "cantidad": "1,332,838.19"
         },
         {
            "nombre": "(+) Depósitos",
            "cantidad": "0.00"
         },
         {
            "nombre": "(-) Retiros",
            "cantidad": "0.00"
         },
         {
            "nombre": "(+)(-) plusvalia",
            "cantidad": "9,973.97"
         },
         {
            "nombre": "(=) Valor de la cartera al corte ",
            "cantidad": "1,342,812.16"
         },
         {
            "nombre": "Total de comisiones cobradas",
            "cantidad": "0.00"
         },
         {
            "nombre": "IVA trasladado comisiones",
            "cantidad": "0.00"
         },
         {
            "nombre": "Comisiones con IVA",
            "cantidad": "0.00"
         }
      ],
      "total_isr": "584.63"
   }

   graficas = fn_generar_graficas_svg(None)
   datos["grafica_pastel"] = graficas.get("grafica_pastel_svg")
   datos["grafica_linea"] = graficas.get("grafica_linea_svg")

   env = Environment(loader = FileSystemLoader("templates"))
   plantilla = env.get_template("layout-resumen.html")
   html = plantilla.render(**datos)

   return html

def fn_crear_tabla_posicion_valores(datos):
   datos = [
      {
         "mes": "enero",
         "anio": "2025",
         "mercado_directo_1": {
            "emisora": "PRUEBA",
            "serie": "PRUEBA1",
            "titulos": "0",
            "costo": "0.000000",
            "precio_mercado": "0.0000000",
            "importe_compra": "1,000,000.00",
            "valor_mercado": "O.OO",
            "plus_minusvalia": "O.00",
            "cartera_total": "10.00"
         },
         "mercado_directo_2": {
            "titulos": "0",
            "importe_compra": "1,000,000.00",
            "valor_mercado": "0.00",
            "plus_minusvalia": "0.00",
            "cartera_total": "10.0"
         },
         "mercado_reporto_1": {
            "emisora": "PRUEBA EMISORA",
            "serie": "123",
            "titulos": "0",
            "fecha_inicio": "2025-01-01",
            "fecha_vencimiento": "2025-01-01",
            "precio_mercado": "10.000000",
            "importe_operacion": "1,300,000.00",
            "valor_cierre": "1,300,000.00",
            "premio_desvengado": "30,000.00",
            "plazo": "0.00",
            "dias_por_vencer": "10.00",
            "tasa": "0.093",
            "cartera_total": "100.00"
         },
         "mercado_reporto_2": {
            "titulos": "154,969",
            "importe_operacion": "1,332,493.10",
            "valor_cierre": "1,332,493.10",
            "premio_desvengado": "344.23",
            "cartera_total": "100.00"
         },
         "mercado_capitales_1": {
            "emisora": "",
            "serie": "",
            "titulos_mes_actual": "0",
            "costo_promedio": "N/A",
            "precio_mercado": "100,000.000000",
            "importe_compra": "0.00",
            "valor_mercado": "0.00",
            "plus_minusvalia": "0.00",
            "cartera_total": "10.00"
         },
         "mercado_capitales_2": {
            "titulos_mes_actual": "0",
            "importe_compra": "0.00",
            "valor_mercado": "0.00",
            "plus_minusvalia": "0.00",
            "cartera_total": "10.00"
         },
         "saldo_efectivo": {
            "moneda": "USD",
            "cantidad": "0",
            "valor_cierre": "10.00",
            "cartera_total": "10.00"
         },
         "total": "1,000,000.00"
      },
      {
         "mes": "enero",
         "anio": "2025",
         "mercado_directo_1": None,
         "mercado_directo_2": {
            "titulos": "0",
            "importe_compra": "1,000,000.00",
            "valor_mercado": "0.00",
            "plus_minusvalia": "0.00",
            "cartera_total": "10.0"
         },
         "mercado_reporto_1": None,
         "mercado_reporto_2": {
            "titulos": "154,969",
            "importe_operacion": "1,332,493.10",
            "valor_cierre": "1,332,493.10",
            "premio_desvengado": "344.23",
            "cartera_total": "100.00"
         },
         "mercado_capitales_1": None,
         "mercado_capitales_2": {
            "titulos_mes_actual": "0",
            "importe_compra": "0.00",
            "valor_mercado": "0.00",
            "plus_minusvalia": "0.00",
            "cartera_total": "10.00"
         },
         "saldo_efectivo": {
            "moneda": "USD",
            "cantidad": "0",
            "valor_cierre": "10.00",
            "cartera_total": "10.00",
         },
         "total": "1,000,000.00"
      },
   ]
   env = Environment(loader = FileSystemLoader("templates"))
   plantilla = env.get_template("layout-posicion-valores.html")
   html = plantilla.render({ "detalles": datos })

   return html

def fn_crear_tabla_movimientos(datos):
   datos = [
      {
         "fecha_operacion": "2024-12-01",
         "fecha_liquidacion": "2024-12-01",
         "tipo_movimiento": "Saldo Inicial",
         "descripcion": "",
         "titulos": 0,
         "plazo": 0,
         "precio": "$0.000000",
         "tasa": "0.000000%",
         "importe_operacion": "$0.86",
         "cargo_abono": "Abono",
         "saldo": "$0.86"
      },
      {
         "fecha_operacion": "2024-11-29",
         "fecha_liquidacion": "2024-12-02",
         "tipo_movimiento": "Vencimiento reporto",
         "descripcion": "BI CETES 260611",
         "titulos": "-154,969",
         "plazo": 3,
         "precio": "$8.598449",
         "tasa": "9.300000%",
         "importe_operacion": "$1,333,525.78",
         "cargo_abono": "Abono",
         "saldo": "$1,333,526.64"
      },
      {
         "fecha_operacion": "2024-11-29",
         "fecha_liquidacion": "2024-12-02",
         "tipo_movimiento": "retención vencimiento reporto",
         "descripcion": "",
         "titulos": 0,
         "plazo": 3,
         "precio": "$0.000000",
         "tasa": "9.300000%",
         "importe_operacion": "$-54.61",
         "cargo_abono": "Cargo",
         "saldo": "$1,333,472.03"
      },
      {
         "fecha_operacion": "2024-12-02",
         "fecha_liquidacion": "2024-12-02",
         "tipo_movimiento": "Inicio Reporto",
         "descripcion": "BI CETES 260611",
         "titulos": "154,960",
         "plazo": 1,
         "precio": "$8.605265",
         "tasa": "9.290000%",
         "importe_operacion": "$-1,333,471.84",
         "cargo_abono": "Cargo",
         "saldo": "$0.19"
      },
      {
         "fecha_operacion": "2024-12-02",
         "fecha_liquidacion": "2024-12-03",
         "tipo_movimiento": "Vencimiento reporto",
         "descripcion": "BI CETES 260611",
         "titulos": "-154,960",
         "plazo": 1,
         "precio": "$8.605265",
         "tasa": "9.290000%",
         "importe_operacion": "$1,333,815.95",
         "cargo_abono": "Abono",
         "saldo": "$1,333,816.14"
      },
      {
         "fecha_operacion": "2024-12-02",
         "fecha_liquidacion": "2024-12-03",
         "tipo_movimiento": "retención vencimiento reporto",
         "descripcion": "",
         "titulos": "0",
         "plazo": 1,
         "precio": "$0.000000",
         "tasa": "9.290000%",
         "importe_operacion": "$-18.22",
         "cargo_abono": "Cargo",
         "saldo": "$1,333,797.92"
      },
      {
         "fecha_operacion": "2024-12-03",
         "fecha_liquidacion": "2024-12-03",
         "tipo_movimiento": "Inicio Reporto",
         "descripcion": "BI CETES 260611",
         "titulos": "154,956",
         "plazo": 1,
         "precio": "$8.607538",
         "tasa": "9.300000%",
         "importe_operacion": "$-1,333,789.64",
         "cargo_abono": "Cargo",
         "saldo": "$8.28"
      },
      {
         "fecha_operacion": "2024-12-03",
         "fecha_liquidacion": "2024-12-04",
         "tipo_movimiento": "Vencimiento reporto",
         "descripcion": "BI CETES 260611",
         "titulos": "-154,956",
         "plazo": 1,
         "precio": "$8.607538",
         "tasa": "9.300000%",
         "importe_operacion": "$1,334,134.20",
         "cargo_abono": "Abono",
         "saldo": "$1,334,142.48"
      },
      {
         "fecha_operacion": "2024-12-03",
         "fecha_liquidacion": "2024-12-04",
         "tipo_movimiento": "retención vencimiento reporto",
         "descripcion": "",
         "titulos": "0",
         "plazo": 1,
         "precio": "$0.000000",
         "tasa": "9.300000%",
         "importe_operacion": "$-18.22",
         "cargo_abono": "Cargo",
         "saldo": "$1,334,124.26"
      },
      {
         "fecha_operacion": "2024-12-04",
         "fecha_liquidacion": "2024-12-04",
         "tipo_movimiento": "Inicio Reporto",
         "descripcion": "BI CETES 260611",
         "titulos": "154,953",
         "plazo": 1,
         "precio": "$8.609812",
         "tasa": "9.280000%",
         "importe_operacion": "$-1334116.12",
         "cargo_abono": "Cargo",
         "saldo": "$8.14"
      },
      {
         "fecha_operacion": "2024-12-04",
         "fecha_liquidacion": "2024-12-05",
         "tipo_movimiento": "Vencimiento reporto",
         "descripcion": "BI CETES 260611",
         "titulos": "-154,953",
         "plazo": 1,
         "precio": "$8.609812",
         "tasa": "9.280000%",
         "importe_operacion": "$1,334,460.03",
         "cargo_abono": "Abono",
         "saldo": "$1,334,468.17"
      },
      {
         "fecha_operacion": "2024-12-04",
         "fecha_liquidacion": "2024-12-05",
         "tipo_movimiento": "retención vencimiento reporto",
         "descripcion": "",
         "titulos": 0,
         "plazo": 1,
         "precio": "$0.000000",
         "tasa": "9.280000%",
         "importe_operacion": "$-18.23",
         "cargo_abono": "Cargo",
         "saldo": "$1,334,449.94"
      },
      {
         "fecha_operacion": "2024-12-05",
         "fecha_liquidacion": "2024-12-05",
         "tipo_movimiento": "Inicio Reporto",
         "descripcion": "BI CETES 260611",
         "titulos": 154950,
         "plazo": 1,
         "precio": "$8.612086",
         "tasa": "9.120000%",
         "importe_operacion": "$-1,334,442.69",
         "cargo_abono": "Cargo",
         "saldo": "$7.25"
      },
      {
         "fecha_operacion": "2024-12-05",
         "fecha_liquidacion": "2024-12-06",
         "tipo_movimiento": "Vencimiento reporto",
         "descripcion": "BI CETES 260611",
         "titulos": "-154,950",
         "plazo": 1,
         "precio": "$8.612086",
         "tasa": "9.120000%",
         "importe_operacion": "1,334,780.75",
         "cargo_abono": "Abono",
         "saldo": "$1,334,788.00"
      },
      {
         "fecha_operacion": "2024-12-05",
         "fecha_liquidacion": "2024-12-06",
         "tipo_movimiento": "retención vencimiento reporto",
         "descripcion": "",
         "titulos": 0,
         "plazo": 1,
         "precio": "$0.000000",
         "tasa": "9.120000%",
         "importe_operacion": "-18.23",
         "cargo_abono": "Cargo",
         "saldo": "$1,334,769.77"
      },
      {
         "fecha_operacion": "2024-12-06",
         "fecha_liquidacion": "2024-12-06",
         "tipo_movimiento": "Inicio Reporto",
         "descripcion": "BI CETES 251224",
         "titulos": "148,183",
         "plazo": 3,
         "precio": "$9.007567",
         "tasa": "9.100000%",
         "importe_operacion": "-1,334,768.28",
         "cargo_abono": "Cargo",
         "saldo": "$1.49"
      },
      {
         "fecha_operacion": "2024-12-06",
         "fecha_liquidacion": "2024-12-09",
         "tipo_movimiento": "Vencimiento reporto",
         "descripcion": "BI CETES 251224",
         "titulos": "-148,183",
         "plazo": 3,
         "precio": "$9.007567",
         "tasa": "9.100000%",
         "importe_operacion": "1,335,780.48",
         "cargo_abono": "Abono",
         "saldo": "$1,335,781.97"
      },
      {
         "fecha_operacion": "2024-12-06",
         "fecha_liquidacion": "2024-12-09",
         "tipo_movimiento": "retención vencimiento reporto",
         "descripcion": "",
         "titulos": 0,
         "plazo": 3,
         "precio": "$0.000000",
         "tasa": "9.100000%",
         "importe_operacion": "-54.70",
         "cargo_abono": "Cargo",
         "saldo": "$1,335,727.27"
      },
      {
         "fecha_operacion": "2024-12-01",
         "fecha_liquidacion": "2024-12-01",
         "tipo_movimiento": "Saldo Inicial",
         "descripcion": "",
         "titulos": 0,
         "plazo": 0,
         "precio": "$0.000000",
         "tasa": "0.000000%",
         "importe_operacion": "$0.86",
         "cargo_abono": "Abono",
         "saldo": "$0.86"
      },
      {
         "fecha_operacion": "2024-11-29",
         "fecha_liquidacion": "2024-12-02",
         "tipo_movimiento": "Vencimiento reporto",
         "descripcion": "BI CETES 260611",
         "titulos": "-154,969",
         "plazo": 3,
         "precio": "$8.598449",
         "tasa": "9.300000%",
         "importe_operacion": "$1,333,525.78",
         "cargo_abono": "Abono",
         "saldo": "$1,333,526.64"
      },
      {
         "fecha_operacion": "2024-11-29",
         "fecha_liquidacion": "2024-12-02",
         "tipo_movimiento": "retención vencimiento reporto",
         "descripcion": "",
         "titulos": 0,
         "plazo": 3,
         "precio": "$0.000000",
         "tasa": "9.300000%",
         "importe_operacion": "$-54.61",
         "cargo_abono": "Cargo",
         "saldo": "$1,333,472.03"
      },
      {
         "fecha_operacion": "2024-12-02",
         "fecha_liquidacion": "2024-12-02",
         "tipo_movimiento": "Inicio Reporto",
         "descripcion": "BI CETES 260611",
         "titulos": "154,960",
         "plazo": 1,
         "precio": "$8.605265",
         "tasa": "9.290000%",
         "importe_operacion": "$-1,333,471.84",
         "cargo_abono": "Cargo",
         "saldo": "$0.19"
      },
      {
         "fecha_operacion": "2024-12-02",
         "fecha_liquidacion": "2024-12-03",
         "tipo_movimiento": "Vencimiento reporto",
         "descripcion": "BI CETES 260611",
         "titulos": "-154,960",
         "plazo": 1,
         "precio": "$8.605265",
         "tasa": "9.290000%",
         "importe_operacion": "$1,333,815.95",
         "cargo_abono": "Abono",
         "saldo": "$1,333,816.14"
      },
      {
         "fecha_operacion": "2024-12-02",
         "fecha_liquidacion": "2024-12-03",
         "tipo_movimiento": "retención vencimiento reporto",
         "descripcion": "",
         "titulos": "0",
         "plazo": 1,
         "precio": "$0.000000",
         "tasa": "9.290000%",
         "importe_operacion": "$-18.22",
         "cargo_abono": "Cargo",
         "saldo": "$1,333,797.92"
      },
      {
         "fecha_operacion": "2024-12-03",
         "fecha_liquidacion": "2024-12-03",
         "tipo_movimiento": "Inicio Reporto",
         "descripcion": "BI CETES 260611",
         "titulos": "154,956",
         "plazo": 1,
         "precio": "$8.607538",
         "tasa": "9.300000%",
         "importe_operacion": "$-1,333,789.64",
         "cargo_abono": "Cargo",
         "saldo": "$8.28"
      },
      {
         "fecha_operacion": "2024-12-03",
         "fecha_liquidacion": "2024-12-04",
         "tipo_movimiento": "Vencimiento reporto",
         "descripcion": "BI CETES 260611",
         "titulos": "-154,956",
         "plazo": 1,
         "precio": "$8.607538",
         "tasa": "9.300000%",
         "importe_operacion": "$1,334,134.20",
         "cargo_abono": "Abono",
         "saldo": "$1,334,142.48"
      },
      {
         "fecha_operacion": "2024-12-03",
         "fecha_liquidacion": "2024-12-04",
         "tipo_movimiento": "retención vencimiento reporto",
         "descripcion": "",
         "titulos": "0",
         "plazo": 1,
         "precio": "$0.000000",
         "tasa": "9.300000%",
         "importe_operacion": "$-18.22",
         "cargo_abono": "Cargo",
         "saldo": "$1,334,124.26"
      },
      {
         "fecha_operacion": "2024-12-04",
         "fecha_liquidacion": "2024-12-04",
         "tipo_movimiento": "Inicio Reporto",
         "descripcion": "BI CETES 260611",
         "titulos": "154,953",
         "plazo": 1,
         "precio": "$8.609812",
         "tasa": "9.280000%",
         "importe_operacion": "$-1334116.12",
         "cargo_abono": "Cargo",
         "saldo": "$8.14"
      },
      {
         "fecha_operacion": "2024-12-04",
         "fecha_liquidacion": "2024-12-05",
         "tipo_movimiento": "Vencimiento reporto",
         "descripcion": "BI CETES 260611",
         "titulos": "-154,953",
         "plazo": 1,
         "precio": "$8.609812",
         "tasa": "9.280000%",
         "importe_operacion": "$1,334,460.03",
         "cargo_abono": "Abono",
         "saldo": "$1,334,468.17"
      },
      {
         "fecha_operacion": "2024-12-04",
         "fecha_liquidacion": "2024-12-05",
         "tipo_movimiento": "retención vencimiento reporto",
         "descripcion": "",
         "titulos": 0,
         "plazo": 1,
         "precio": "$0.000000",
         "tasa": "9.280000%",
         "importe_operacion": "$-18.23",
         "cargo_abono": "Cargo",
         "saldo": "$1,334,449.94"
      },
      {
         "fecha_operacion": "2024-12-05",
         "fecha_liquidacion": "2024-12-05",
         "tipo_movimiento": "Inicio Reporto",
         "descripcion": "BI CETES 260611",
         "titulos": 154950,
         "plazo": 1,
         "precio": "$8.612086",
         "tasa": "9.120000%",
         "importe_operacion": "$-1,334,442.69",
         "cargo_abono": "Cargo",
         "saldo": "$7.25"
      },
      {
         "fecha_operacion": "2024-12-05",
         "fecha_liquidacion": "2024-12-06",
         "tipo_movimiento": "Vencimiento reporto",
         "descripcion": "BI CETES 260611",
         "titulos": "-154,950",
         "plazo": 1,
         "precio": "$8.612086",
         "tasa": "9.120000%",
         "importe_operacion": "1,334,780.75",
         "cargo_abono": "Abono",
         "saldo": "$1,334,788.00"
      },
      {
         "fecha_operacion": "2024-12-05",
         "fecha_liquidacion": "2024-12-06",
         "tipo_movimiento": "retención vencimiento reporto",
         "descripcion": "",
         "titulos": 0,
         "plazo": 1,
         "precio": "$0.000000",
         "tasa": "9.120000%",
         "importe_operacion": "-18.23",
         "cargo_abono": "Cargo",
         "saldo": "$1,334,769.77"
      },
      {
         "fecha_operacion": "2024-12-06",
         "fecha_liquidacion": "2024-12-06",
         "tipo_movimiento": "Inicio Reporto",
         "descripcion": "BI CETES 251224",
         "titulos": "148,183",
         "plazo": 3,
         "precio": "$9.007567",
         "tasa": "9.100000%",
         "importe_operacion": "-1,334,768.28",
         "cargo_abono": "Cargo",
         "saldo": "$1.49"
      },
      {
         "fecha_operacion": "2024-12-06",
         "fecha_liquidacion": "2024-12-09",
         "tipo_movimiento": "Vencimiento reporto",
         "descripcion": "BI CETES 251224",
         "titulos": "-148,183",
         "plazo": 3,
         "precio": "$9.007567",
         "tasa": "9.100000%",
         "importe_operacion": "1,335,780.48",
         "cargo_abono": "Abono",
         "saldo": "$1,335,781.97"
      },
      {
         "fecha_operacion": "2024-12-06",
         "fecha_liquidacion": "2024-12-09",
         "tipo_movimiento": "retención vencimiento reporto",
         "descripcion": "",
         "titulos": 0,
         "plazo": 3,
         "precio": "$0.000000",
         "tasa": "9.100000%",
         "importe_operacion": "-54.70",
         "cargo_abono": "Cargo",
         "saldo": "$1,335,727.27"
      },
      {
         "fecha_operacion": "2024-12-01",
         "fecha_liquidacion": "2024-12-01",
         "tipo_movimiento": "Saldo Inicial",
         "descripcion": "",
         "titulos": 0,
         "plazo": 0,
         "precio": "$0.000000",
         "tasa": "0.000000%",
         "importe_operacion": "$0.86",
         "cargo_abono": "Abono",
         "saldo": "$0.86"
      },
      {
         "fecha_operacion": "2024-11-29",
         "fecha_liquidacion": "2024-12-02",
         "tipo_movimiento": "Vencimiento reporto",
         "descripcion": "BI CETES 260611",
         "titulos": "-154,969",
         "plazo": 3,
         "precio": "$8.598449",
         "tasa": "9.300000%",
         "importe_operacion": "$1,333,525.78",
         "cargo_abono": "Abono",
         "saldo": "$1,333,526.64"
      },
      {
         "fecha_operacion": "2024-11-29",
         "fecha_liquidacion": "2024-12-02",
         "tipo_movimiento": "retención vencimiento reporto",
         "descripcion": "",
         "titulos": 0,
         "plazo": 3,
         "precio": "$0.000000",
         "tasa": "9.300000%",
         "importe_operacion": "$-54.61",
         "cargo_abono": "Cargo",
         "saldo": "$1,333,472.03"
      },
      {
         "fecha_operacion": "2024-12-02",
         "fecha_liquidacion": "2024-12-02",
         "tipo_movimiento": "Inicio Reporto",
         "descripcion": "BI CETES 260611",
         "titulos": "154,960",
         "plazo": 1,
         "precio": "$8.605265",
         "tasa": "9.290000%",
         "importe_operacion": "$-1,333,471.84",
         "cargo_abono": "Cargo",
         "saldo": "$0.19"
      },
      {
         "fecha_operacion": "2024-12-02",
         "fecha_liquidacion": "2024-12-03",
         "tipo_movimiento": "Vencimiento reporto",
         "descripcion": "BI CETES 260611",
         "titulos": "-154,960",
         "plazo": 1,
         "precio": "$8.605265",
         "tasa": "9.290000%",
         "importe_operacion": "$1,333,815.95",
         "cargo_abono": "Abono",
         "saldo": "$1,333,816.14"
      },
      {
         "fecha_operacion": "2024-12-02",
         "fecha_liquidacion": "2024-12-03",
         "tipo_movimiento": "retención vencimiento reporto",
         "descripcion": "",
         "titulos": "0",
         "plazo": 1,
         "precio": "$0.000000",
         "tasa": "9.290000%",
         "importe_operacion": "$-18.22",
         "cargo_abono": "Cargo",
         "saldo": "$1,333,797.92"
      },
      {
         "fecha_operacion": "2024-12-03",
         "fecha_liquidacion": "2024-12-03",
         "tipo_movimiento": "Inicio Reporto",
         "descripcion": "BI CETES 260611",
         "titulos": "154,956",
         "plazo": 1,
         "precio": "$8.607538",
         "tasa": "9.300000%",
         "importe_operacion": "$-1,333,789.64",
         "cargo_abono": "Cargo",
         "saldo": "$8.28"
      },
      {
         "fecha_operacion": "2024-12-03",
         "fecha_liquidacion": "2024-12-04",
         "tipo_movimiento": "Vencimiento reporto",
         "descripcion": "BI CETES 260611",
         "titulos": "-154,956",
         "plazo": 1,
         "precio": "$8.607538",
         "tasa": "9.300000%",
         "importe_operacion": "$1,334,134.20",
         "cargo_abono": "Abono",
         "saldo": "$1,334,142.48"
      },
      {
         "fecha_operacion": "2024-12-03",
         "fecha_liquidacion": "2024-12-04",
         "tipo_movimiento": "retención vencimiento reporto",
         "descripcion": "",
         "titulos": "0",
         "plazo": 1,
         "precio": "$0.000000",
         "tasa": "9.300000%",
         "importe_operacion": "$-18.22",
         "cargo_abono": "Cargo",
         "saldo": "$1,334,124.26"
      },
      {
         "fecha_operacion": "2024-12-04",
         "fecha_liquidacion": "2024-12-04",
         "tipo_movimiento": "Inicio Reporto",
         "descripcion": "BI CETES 260611",
         "titulos": "154,953",
         "plazo": 1,
         "precio": "$8.609812",
         "tasa": "9.280000%",
         "importe_operacion": "$-1334116.12",
         "cargo_abono": "Cargo",
         "saldo": "$8.14"
      },
      {
         "fecha_operacion": "2024-12-04",
         "fecha_liquidacion": "2024-12-05",
         "tipo_movimiento": "Vencimiento reporto",
         "descripcion": "BI CETES 260611",
         "titulos": "-154,953",
         "plazo": 1,
         "precio": "$8.609812",
         "tasa": "9.280000%",
         "importe_operacion": "$1,334,460.03",
         "cargo_abono": "Abono",
         "saldo": "$1,334,468.17"
      },
      {
         "fecha_operacion": "2024-12-04",
         "fecha_liquidacion": "2024-12-05",
         "tipo_movimiento": "retención vencimiento reporto",
         "descripcion": "",
         "titulos": 0,
         "plazo": 1,
         "precio": "$0.000000",
         "tasa": "9.280000%",
         "importe_operacion": "$-18.23",
         "cargo_abono": "Cargo",
         "saldo": "$1,334,449.94"
      },
      {
         "fecha_operacion": "2024-12-05",
         "fecha_liquidacion": "2024-12-05",
         "tipo_movimiento": "Inicio Reporto",
         "descripcion": "BI CETES 260611",
         "titulos": 154950,
         "plazo": 1,
         "precio": "$8.612086",
         "tasa": "9.120000%",
         "importe_operacion": "$-1,334,442.69",
         "cargo_abono": "Cargo",
         "saldo": "$7.25"
      },
      {
         "fecha_operacion": "2024-12-05",
         "fecha_liquidacion": "2024-12-06",
         "tipo_movimiento": "Vencimiento reporto",
         "descripcion": "BI CETES 260611",
         "titulos": "-154,950",
         "plazo": 1,
         "precio": "$8.612086",
         "tasa": "9.120000%",
         "importe_operacion": "1,334,780.75",
         "cargo_abono": "Abono",
         "saldo": "$1,334,788.00"
      },
      {
         "fecha_operacion": "2024-12-05",
         "fecha_liquidacion": "2024-12-06",
         "tipo_movimiento": "retención vencimiento reporto",
         "descripcion": "",
         "titulos": 0,
         "plazo": 1,
         "precio": "$0.000000",
         "tasa": "9.120000%",
         "importe_operacion": "-18.23",
         "cargo_abono": "Cargo",
         "saldo": "$1,334,769.77"
      },
      {
         "fecha_operacion": "2024-12-06",
         "fecha_liquidacion": "2024-12-06",
         "tipo_movimiento": "Inicio Reporto",
         "descripcion": "BI CETES 251224",
         "titulos": "148,183",
         "plazo": 3,
         "precio": "$9.007567",
         "tasa": "9.100000%",
         "importe_operacion": "-1,334,768.28",
         "cargo_abono": "Cargo",
         "saldo": "$1.49"
      },
      {
         "fecha_operacion": "2024-12-06",
         "fecha_liquidacion": "2024-12-09",
         "tipo_movimiento": "Vencimiento reporto",
         "descripcion": "BI CETES 251224",
         "titulos": "-148,183",
         "plazo": 3,
         "precio": "$9.007567",
         "tasa": "9.100000%",
         "importe_operacion": "1,335,780.48",
         "cargo_abono": "Abono",
         "saldo": "$1,335,781.97"
      },
      {
         "fecha_operacion": "2024-12-06",
         "fecha_liquidacion": "2024-12-09",
         "tipo_movimiento": "retención vencimiento reporto",
         "descripcion": "",
         "titulos": 0,
         "plazo": 3,
         "precio": "$0.000000",
         "tasa": "9.100000%",
         "importe_operacion": "-54.70",
         "cargo_abono": "Cargo",
         "saldo": "$1,335,727.27"
      }
   ]

   env = Environment(loader = FileSystemLoader("templates"))
   plantilla = env.get_template("layout-movimientos.html")
   html = plantilla.render({ "movimientos": datos })

   return html

def fn_crear_diferencial_1(datos):
   datos = {
      "mes": "enero",
      "anio": "2025",
      "detalle": {
         "mercado_directo_1": {
            "tipo_posicion": "A",
            "emisora": "LF BONDESF 251023",
            "serie": "251023",
            "titulos": "10,000",
            "costo": "1,000,000.000000",
            "precio_anterior": "0.000000",
            "precio_actual": "1,000,000.000000",
            "diferencial_valuacion": "0.00",
            "porcentaje": "0.00"
         },
         "mercado_directo_2": {
            "titulos": "0",
            "diferencial_valuacion": "0.00"
         },
         "mercado_reporto_1": {
            "tipo_posicion": "B",
            "emisora": "LF BONDESF 251024",
            "serie": "251024",
            "titulos": "10,000",
            "costo": "1,000,000.000000",
            "precio_anterior": "0.000000",
            "precio_actual": "1,000,000.000000",
            "diferencial_valuacion": "0.00",
            "porcentaje": "0.00"
         },
         "mercado_reporto_2": {
            "titulos": "1",
            "diferencial_valuacion": "1.00"
         },
         "mercado_capitales_1": None,
         "mercado_capitales_2": {
            "titulos": "2",
            "diferencial_valuacion": "0.00"
         }
      }
   }

   env = Environment(loader = FileSystemLoader("templates"))
   plantilla = env.get_template("layout-diferencial-1.html")
   html = plantilla.render(datos)

   return html

def fn_crear_diferencial_2(datos):
   datos = {
      "mes": "enero",
      "anio": "2025",
      "detalle": {
         "mercado_directo_1": {
            "tipo_posicion": "A",
            "emisora": "LF BONDESF 251023",
            "serie": "251023",
            "titulos": "10,000",
            "costo": "1,000,000.000000",
            "precio_venta": "0.000000",
            "diferencial_valuacion": "0.00",
            "porcentaje": "0.00"
         },
         "mercado_directo_2": {
            "titulos": "0",
            "diferencial_valuacion": "0.00"
         },
         "mercado_reporto_1": {
            "tipo_posicion": "A",
            "emisora": "LF BONDESF 251023",
            "serie": "251023",
            "titulos": "10,000",
            "costo": "1,000,000.000000",
            "precio_venta": "0.000000",
            "diferencial_valuacion": "0.00",
            "porcentaje": "0.00"
         },
         "mercado_reporto_2": {
            "titulos": "1",
            "diferencial_valuacion": "1.00"
         },
         "mercado_capitales_1": None,
         "mercado_capitales_2": {
            "titulos": "2",
            "diferencial_valuacion": "0.00"
         }
      }
   }

   env = Environment(loader = FileSystemLoader("templates"))
   plantilla = env.get_template("layout-diferencial-2.html")
   html = plantilla.render(datos)

   return html

def fn_crear_tabla_rendimiento_cartera_inversion(datos):
   datos = [
      {
         "Mes": "ENE",
         "valor_cartera": "$1,231,238.97",
         "rendimiento_periodo": "$10,810.14",
         "porcentaje_bruto": "0.88%",
         "rendimiento_neto": "$10,258.02",
         "porcentaje_neto": "0.83%"
      },
      {
         "Mes": "FEB",
         "valor_cartera": "$1,240,937.80",
         "rendimiento_periodo": "$10,188.39",
         "porcentaje_bruto": "0.82%",
         "rendimiento_neto": "$9,698.83",
         "porcentaje_neto": "0.78%"
      },
      {
         "Mes": "MAR",
         "valor_cartera": "$1,251,391.85",
         "rendimiento_periodo": "$10,913.29",
         "porcentaje_bruto": "0.87%",
         "rendimiento_neto": "$10,454.05",
         "porcentaje_neto": "0.84%"
      },
      {
         "Mes": "ABR",
         "valor_cartera": "$1,261,271.25",
         "rendimiento_periodo": "$10,462.41",
         "porcentaje_bruto": "0.83%",
         "rendimiento_neto": "$9,879.39",
         "porcentaje_neto": "0.78%"
      },
      {
         "Mes": "MAY",
         "valor_cartera": "$1,271,638.46",
         "rendimiento_periodo": "$10,903.42",
         "porcentaje_bruto": "0.86%",
         "rendimiento_neto": "$10,367.22",
         "porcentaje_neto": "0.82%"
      },
      {
         "Mes": "JUN",
         "valor_cartera": "$1,281,790.46",
         "rendimiento_periodo": "$10,640.08",
         "porcentaje_bruto": "0.83%",
         "rendimiento_neto": "$10,152.00",
         "porcentaje_neto": "0.79%"
      },
      {
         "Mes": "JUL",
         "valor_cartera": "$1,292,295.22",
         "rendimiento_periodo": "$11,084.65",
         "porcentaje_bruto": "0.86%",
         "rendimiento_neto": "$10,504.76",
         "porcentaje_neto": "0.81%"
      },
      {
         "Mes": "AGO",
         "valor_cartera": "$1,302,739.58",
         "rendimiento_periodo": "$10,975.92",
         "porcentaje_bruto": "0.84%",
         "rendimiento_neto": "$10,444.35",
         "porcentaje_neto": "0.80%"
      },
      {
         "Mes": "SEP",
         "valor_cartera": "$1,312,771.64",
         "rendimiento_periodo": "$10,585.64",
         "porcentaje_bruto": "0.81%",
         "rendimiento_neto": "$10,032.06",
         "porcentaje_neto": "0.76%"
      },
      {
         "Mes": "OCT",
         "valor_cartera": "$1,322,987.66",
         "rendimiento_periodo": "$10,774.01",
         "porcentaje_bruto": "0.81%",
         "rendimiento_neto": "$10,216.02",
         "porcentaje_neto": "0.77%"
      },
      {
         "Mes": "NOV",
         "valor_cartera": "$1,332,838.19",
         "rendimiento_periodo": "$10,376.43",
         "porcentaje_bruto": "0.78%",
         "rendimiento_neto": "$9,850.53",
         "porcentaje_neto": "0.74%"
      },
      {
         "Mes": "DIC",
         "valor_cartera": "$1,342,812.16",
         "rendimiento_periodo": "$10,558.60",
         "porcentaje_bruto": "0.79%",
         "rendimiento_neto": "$9,973.97",
         "porcentaje_neto": "0.74%"
      }
   ]
   mes_rendimiento = "enero"
   anio_rendimiento = "2025"

   env = Environment(loader = FileSystemLoader("templates"))
   plantilla = env.get_template("layout-rendimiento-desglose.html")
   html = plantilla.render({
      "datos": datos,
      "mes_rendimiento": mes_rendimiento,
      "anio_rendimiento": anio_rendimiento
   })

   return html

def fn_crear_tabla_avisos(avisos):
   avisos = [
      """
         Cualquier aclaración relacionada con la información contenida en el presente estado de cuenta, deberá ser notificada
         a nuestra Unidad Especializada de Atención a Usuarios al teléfono 55 8659 5300 o por correo electrónico a la dirección
         une@altorcb.com dentro de los 60 días naturales siguientes a su fecha de corte, de lo contrario se tendrán por aceptadas
         y consentidas las posiciones de valores, los movimientos y los saldos que éste contiene. Sin perjuicio de lo anterior,
         usted podrá presentar su reclamación en los términos de la regulación aplicable ante la CONDUSEF, Comisión Nacional para
         la Protección y Defensa de los Usuarios de Servicios Financieros al teléfono 55 5340 0999 ó 800 999 8080 o a través de la
         página www.condusef.gob.mx
      """
   ]
   env = Environment(loader = FileSystemLoader("templates"))
   plantilla = env.get_template("layout-avisos.html")
   html = plantilla.render({ "avisos": avisos })

   return html

def fn_crear_tabla_glosario(datos):
   datos = [
      ("Cta", "Cuenta(s)"),
      ("MXN", "Pesos Mexicanos"),
      ("Núm", "Número"),
      ("F. Inic", "Fecha de inicio"),
      ("F. Venc.", "Fecha de Vencimiento"),
      ("SIC", "Sistema Internacional de Cotizaciones"),
      ("CFDI", "Comprobante Fiscal Digital por Internet"),
      ("UUID", "Identificador Universalmente Único"),
      ("ISR", "Impuesto Sobre la Renta"),
      ("IVA", "Impuesto al Valor Agregado"),
      ("ENE", "Enero"),
      ("FEB", "Febrero"),
      ("MAR", "Marzo"),
      ("ABR", "Abril"),
      ("MAY", "Mayo"),
      ("JUN", "Junio"),
      ("JUL", "Julio"),
      ("AGO", "Agosto"),
      ("SEP", "Septiembre"),
      ("OCT", "Octubre"),
      ("NOV", "Noviembre"),
      ("DIC", "Diciembre"),
      ("MC", "Mercado Capitales"),
      ("MD", "Mercado de Dinero"),
      ("RFC", "Registro Federal de Contribuyentes"),
      ("SAT", "Sistema de Administración Tributaria"),
      ("CNBV", "Comisión Nacional Bancarai y de Valores"),
      ("Núm", "Número"),
      ("CDMX", "Ciudad de México"),
      ("CKDs", "Certificados De Capital de Desarrollo")
   ]

   env = Environment(loader = FileSystemLoader("templates"))
   plantilla = env.get_template("layout-glosario.html")
   html = plantilla.render({ "datos": datos })

   return html

def fn_crear_tabla_facturacion(datos):
   datos = {
      "cantidad": "1.00",
      "clave_unidad": "E49",
      "clave_producto": "84121500",
      "descripcion": "Servicio de facturación",
      "valor_unitario": "0.01",
      "total_importe": "0.01",
      "tasa_iva": "0.16000",
      "subtotal": "0.01",
      "iva": "0.00",
      "importe_total": "0.01",
      "sello_cfdi": "Ugr38wooihyhTWuqz0VgNWG/1AyZhIn3GJzO/ZxukXQadxwXxmPyBa7kTy7BpKK1aq30xRWy98sTmZVA27Om1/fmfmBPL+4F7h2XLROEnTQSdkFZQPPwW/ef3EKddypGT4Q2DRdiLrItUiWNqrk8R6BcSipIHANKrhOjKjovqXJGsQvXv9s+3HEYp33jrAy8MJYG4FUCTwTDo7VB4FHrmU3W41GtAUC9Ho0h1kDClLn2VgQt3m+WhplTmUl8jkII86aRvJyjc2V4xLhOYJQn0eHmrHVPGoNjFVHzMskQw8ZO9Miev+WHx1QLUddN+vx6NPG9aa0Ht94runNYhWYTdg==",
      "sello_sat": "QFjFe8nXnuV3QrNd9YF0A0XRmRrTHEwHlxUojMdflK8E/dbIbIlBK73eXcE+2CUIiqDcIsQ6l5qyfieO3jYO8umJ3UnNKGCfkzf62Ta3FGNu5cu8khRh5YTzJu7WTCx/VDD3R18q4BTskLlqw1cpHdlaOcqb yfFDlRecTCj6qDaSmIfeefpYpSRw==",
      "cadena_original": "|1.1|B002E166-B5AE-E549-A1C5-BA18D1ECFE9A|2025-01-07T20:16:30|SCD110105654|Ugr38wooihyhTWuqz0VgNWG/1AyZhIn3GJzO/ZxukXQadxwXxmPyBa7kTy7BpKK1aq30xRWy98sTmZVA27Om1/fmfmBPL+4F7h2XLROEnTQSdkFZQPPwW/ef3EKddypGT4Q2DRdiLrItUiWNqrk8R6BcSipIHANKrhOjKjovqXJGsQvXv9s+3HEYp33jrAy8MJYG4FUCTwTDo7VB4FHrmU3W41GtAUC9Ho0h1kDClLn 2VgQt3m+WhplTmUl8jkII86aRvJyjc2V4xLhOYJQn0eHmrHVPGoNjFVHzMskQw8ZO9Miev+WHx1QLUddN+vx6NPG9aa0Ht94runNYhWYTdg==|00001000000702501858||",
      "razon_social_emisor": "ALTOR CASA DE BOLSA",
      "rfc_emisor": "XAXX010101000",
      "regimen_emisor": "601",
      "lugar_expedicion": "05120",
      "fecha_expedicion": "2025-01-07T19:48:45",
      "metodo_pago": "PUE",
      "forma_pago": "03",
      "folio_fiscal": "B002E166-B5AE-E549-A1C5-BA18D1ECFE9A",
      "num_serie_sat": "00001000000702501858",
      "num_serie_emisor": "00001000000702501859",
      "fecha_hora_certificacion": "07/01/2025 08:16:30 p. m."
   }

   env = Environment(loader = FileSystemLoader("templates"))
   plantilla = env.get_template("layout-cfdi.html")
   html = plantilla.render(**datos)

   return html

def main(indice):
   try:
      paginas = []
      hoja_resumen = fn_crear_tabla_resumen()
      hoja_posicion_valores = fn_crear_tabla_posicion_valores(None)
      hoja_movimientos = fn_crear_tabla_movimientos(None)
      # En vez de hacer append probar concatenando la cadena a la hoja anterior
      hoja_diferencial_1 = fn_crear_diferencial_1(None)
      hoja_diferencial_2 = fn_crear_diferencial_2(None)
      hoja_rendimientos = fn_crear_tabla_rendimiento_cartera_inversion(None)
      hoja_avisos = fn_crear_tabla_avisos(None)
      hoja_glosario = fn_crear_tabla_glosario(None)
      hoja_cfdi = fn_crear_tabla_facturacion(None)

      if hoja_resumen:
         paginas.append(hoja_resumen)
      if hoja_posicion_valores:
         paginas.append(hoja_posicion_valores)
      if hoja_movimientos:
         paginas.append(hoja_movimientos)
      if hoja_diferencial_1:
         paginas.append(hoja_diferencial_1)
      if hoja_diferencial_2:
         paginas.append(hoja_diferencial_2)
      if hoja_rendimientos:
         paginas.append(hoja_rendimientos)
      if hoja_avisos:
         paginas.append(hoja_avisos)
      if hoja_glosario:
         paginas.append(hoja_glosario)
      if hoja_cfdi:
         paginas.append(hoja_cfdi)

      fn_generar_pdf(paginas, indice)

   except Exception as e:
      import traceback
      traceback.print_exc()


if __name__ == "__main__":
   for i in range(1):
      main(i)
      print(f"Ciclo número {i}")