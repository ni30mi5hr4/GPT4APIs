#!/bin/bash

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to display response in a rectangular box
display_response() {
  local response="$1"
  printf "${YELLOW}%s\n" "$response"
}

# Function to display menu
display_menu() {
  printf "\n${CYAN}MENU:\n"
  printf "${CYAN}1. ${GREEN}Enter a question\n"
  printf "${CYAN}2. ${GREEN}Clear screen\n"
  printf "${CYAN}3. ${GREEN}Exit\n"
  printf "Enter your choice: ${NC}"
}

# Main loop
while true; do
  printf "${CYAN}Enter your question directly or choose from the menu options:\n"
  printf "${CYAN}1. ${BLUE}Enter a question\n"
  printf "${CYAN}2. ${BLUE}Clear screen\n"
  printf "${CYAN}3. ${BLUE}Exit\n"
  printf "${RED}Your choice or Ask your question directly: ${NC}"

  read choice_or_question

  case $choice_or_question in
    1)
      printf "${CYAN}Enter your question: ${NC}"
      read question
      ;;
    2)
      clear
      continue
      ;;
    3)
      printf "${CYAN}Exiting Program, Goodbye!${NC}\n"
      exit 0
      ;;
    *)
      question=$choice_or_question
      ;;
  esac

  # API endpoint and headers
  url='https://api.blackbox.ai/api/chat'
  headers='Cookie: sessionId=dc6b94e8-4cb3-44d0-a00f-345c1083e374; personalId=dc6b94e8-4cb3-44d0-a00f-345c1083e374; g_state={"i_p":1710667247859,"i_l":1}; intercom-id-jlmqxicb=f284bc17-3c0a-4712-8947-eca99bb21b93; intercom-session-jlmqxicb=; intercom-device-id-jlmqxicb=45db7d96-3a0b-486d-8fcd-10ce8f887836'
  headers+=' User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0'
  headers+=' Accept: */*'
  headers+=' Accept-Language: en-US,en;q=0.5'
  headers+=' Accept-Encoding: gzip, deflate, br'
  headers+=' Referer: https://www.blackbox.ai/'
  headers+=' Content-Type: application/json'
  headers+=' Origin: https://www.blackbox.ai'
  headers+=' Sec-Fetch-Dest: empty'
  headers+=' Sec-Fetch-Mode: cors'
  headers+=' Sec-Fetch-Site: same-origin'
  headers+=' Te: trailers'

  # Include input in JSON data
  data='{"messages":[{"id":"36eCoH9","content":"'"$question"'","role":"user"}],"id":"36eCoH9","previewToken":null,"userId":"a9595e73-d057-49ed-9c32-8fac0efa32b2","codeModelMode":true,"agentMode":{},"trendingAgentMode":{},"isMicMode":false,"isChromeExt":false,"githubToken":null}'

  # Send POST request and display response
  printf "${CYAN}Processing your request...${NC}"
  spinner="/-\\|"
  while :; do
      for (( i=0; i<${#spinner}; i++ )); do
          printf "%s\b" "${spinner:i:1}"
          sleep 0.1
      done
  done &

  spinner_pid=$!

  response=$(curl -s -X POST -H "$headers" -d "$data" "$url")

  kill $spinner_pid &> /dev/null
  printf "\b" # clear spinner
  clear
  display_response "$response"

  # Wait for user to press Enter before clearing the screen
  printf "${CYAN}\nPress Enter to continue...${NC}"
  read -r
  clear
done
