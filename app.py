import streamlit as st
from core.elastic import init_es
from ui.dashboard import render

init_es()
render()
