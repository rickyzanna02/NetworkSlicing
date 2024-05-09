import io
import base64
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import sys
import networkx as nx
import matplotlib.pyplot as plt
import webbrowser
import sys
sys.path.append('.')
param = sys.argv[1]

# Creazione di un grafo
G = nx.Graph()

# Aggiunta dei nodi switch
switches = ['S1', 'S2']
G.add_nodes_from(switches)

# Aggiunta dei nodi host per lo switch 1
hosts_switch1 = ['h1', 'h2', 'h3']
for host in hosts_switch1:
    G.add_node(host)
    G.add_edge('S1', host)

# Aggiunta dei nodi host per lo switch 2
hosts_switch2 = ['h4', 'h5', 'h6']
for host in hosts_switch2:
    G.add_node(host)
    G.add_edge('S2', host)

# Collegamento tra i due switch
G.add_edge('S1', 'S2')

# Definizione dello stile e dello spessore degli archi
connected = ('solid', 2.0, 'red')
not_connected = ('dashed', 1.0, 'black')

if(param == "a"):
    edge_styles = {('S1', 'h1'): connected,
                ('S1', 'h2'): connected,
                ('S1', 'h3'): not_connected,
                ('S2', 'h4'): connected,
                ('S2', 'h5'): connected,
                ('S2', 'h6'): not_connected,
                ('S1', 'S2'): connected}
elif(param == "b"):
    edge_styles = {('S1', 'h1'): connected,
                ('S1', 'h2'): connected,
                ('S1', 'h3'): connected,
                ('S2', 'h4'): connected,
                ('S2', 'h5'): connected,
                ('S2', 'h6'): connected,
                ('S1', 'S2'): connected}
elif(param == "c1"):
    edge_styles = {('S1', 'h1'): connected,
                ('S1', 'h2'): not_connected,
                ('S1', 'h3'): not_connected,
                ('S2', 'h4'): connected,
                ('S2', 'h5'): not_connected,
                ('S2', 'h6'): not_connected,
                ('S1', 'S2'): connected}
elif(param == "c2"):
    edge_styles = {('S1', 'h1'): not_connected,
                ('S1', 'h2'): connected,
                ('S1', 'h3'): not_connected,
                ('S2', 'h4'): not_connected,
                ('S2', 'h5'): connected,
                ('S2', 'h6'): not_connected,
                ('S1', 'S2'): connected}
elif(param == "c3"):
    edge_styles = {('S1', 'h1'): not_connected,
                ('S1', 'h2'): not_connected,
                ('S1', 'h3'): connected,
                ('S2', 'h4'): not_connected,
                ('S2', 'h5'): not_connected,
                ('S2', 'h6'): connected,
                ('S1', 'S2'): connected}

# Funzione per generare l'immagine del grafico e restituire il codice HTML per visualizzarlo
def generate_graph():
    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G)

    nx.draw_networkx_nodes(G, pos, nodelist=switches, node_shape='s', node_size=700, node_color='blue')
    nx.draw_networkx_nodes(G, pos, nodelist=['h1', 'h4'], node_shape='o', node_size=700, node_color='green')  # h1 e h4 verde
    nx.draw_networkx_nodes(G, pos, nodelist=['h2', 'h5'], node_shape='o', node_size=700, node_color='yellow') # h2 e h5 giallo
    nx.draw_networkx_nodes(G, pos, nodelist=['h3', 'h6'], node_shape='o', node_size=700, node_color='purple') # h3 e h6 viola

    for edge, (style, width, color) in edge_styles.items():
        nx.draw_networkx_edges(G, pos, edgelist=[edge], width=width, style=style, edge_color=color)

    nx.draw_networkx_labels(G, pos)

        # Aggiungi la legenda degli host
    legend_colors = {'h1': 'green', 'h2': 'yellow', 'h3': 'purple'}
    legend_labels = {'h1': 'Slice 1', 'h2': 'Slice 2', 'h3': 'Slice 3'}
    for host, color in legend_colors.items():
        plt.scatter([], [], color=color, label=legend_labels[host], s=200)
        plt.scatter([], [], color='none', label='     ') 

    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize='large', markerscale=1.5)

    plt.title("Network Topology")
    plt.axis('off')

    plt.subplots_adjust(right=0.7)

    # Salva l'immagine in memoria come base64
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    plt.close()

    # Codifica l'immagine in base64
    return base64.b64encode(buf.getvalue()).decode('utf-8')

# Classe per gestire le richieste HTTP
class HTTPRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Genera il codice HTML che include l'immagine del grafico
        html_content = f"""
        <html>
        <head>
            <title>Network Topology</title>
        </head>
        <body>
            <img src="data:image/png;base64,{generate_graph()}" />
        </body>
        </html>
        """

        # Invia la risposta HTTP
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))

        # Termina il server dopo aver gestito la prima richiesta
        threading.Thread(target=self.server.shutdown).start()

# Funzione per avviare il server HTTP
def run_server(port=8080):
    server_address = ('', port)
    httpd = HTTPServer(server_address, HTTPRequestHandler)
    print(f'Server avviato su http://localhost:{port}')
    webbrowser.open("http://localhost:8080")

    httpd.serve_forever()

if __name__ == '__main__':
    run_server()    
