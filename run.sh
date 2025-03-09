
#!/bin/bash

# Display menu
echo "HomeBridge: UBC International Student Support"
echo "--------------------------------------------"
echo "1. Run Flask web application"
echo "2. Run Streamlit dashboard"
echo "3. Exit"
echo ""
read -p "Enter your choice [1-3]: " choice

case $choice in
    1)
        echo "Starting Flask application..."
        python main.py
        ;;
    2)
        echo "Starting Streamlit dashboard..."
        streamlit run streamlit_app.py
        ;;
    3)
        echo "Exiting..."
        exit 0
        ;;
    *)
        echo "Invalid choice. Exiting..."
        exit 1
        ;;
esac
