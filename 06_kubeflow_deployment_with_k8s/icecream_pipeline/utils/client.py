import kfp

def get_kfp_client():
    # Replace with your actual VM IP address
    host_url = "http://192.168.1.100:31380"
    return kfp.Client(host=host_url)
