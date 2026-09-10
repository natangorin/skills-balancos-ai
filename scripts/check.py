#!/usr/bin/env python3
"""Valida as skills deste repositório contra o padrão Agent Skills e as regras da casa.

Reprova quando:
- SKILL.md sem frontmatter, sem `name` ou sem `description`;
- `name` diferente do nome da pasta, fora de [a-z0-9-] ou com hífen duplo;
- `description` vazia ou acima de 1024 caracteres;
- valor do frontmatter com ": " sem aspas (YAML inválido; `npx skills add` pula a skill);
- SKILL.md acima de 500 linhas;
- nome com cara de tool citado em crase (`buscar_x`, `ranking_y`...) que não existe no MCP;
- link http(s) para domínio fora da lista permitida;
- arquivo referenciado como `references/...` que não existe.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SKILLS = RAIZ / "skills"

TOOLS_DO_MCP = {
    "buscar_empresas",
    "ficha_empresa",
    "balancos_empresa",
    "dres_empresa",
    "documentos_empresa",
    "texto_documento",
    "ranking_empresas",
    "analisar_empresa",
}
DOMINIOS_PERMITIDOS = {
    "balancos.ai",
    "mcp.balancos.ai",
    "api.balancos.ai",
    "github.com",
    "agentskills.io",
    "code.claude.com",
    "claude.ai",
    "support.claude.com",
    "modelcontextprotocol.io",
    "registry.modelcontextprotocol.io",
}
RE_NOME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")
RE_TOOL = re.compile(
    r"`((?:buscar|ficha|balancos|dres|documentos|texto|ranking|analisar|listar|comparar|"
    r"pares|novidades|contar|filtrar|empresas|setores)_[a-z_]+)(?:\([^)]*\))?`"
)
RE_LINK = re.compile(r"https?://([a-zA-Z0-9-]+(?:\.[a-zA-Z0-9-]+)+)")
RE_REF = re.compile(r"\(((?:references|assets|scripts)/[^)\s]+)\)")


def frontmatter(texto: str) -> dict[str, str] | None:
    if not texto.startswith("---\n"):
        return None
    fim = texto.find("\n---", 4)
    if fim < 0:
        return None
    campos: dict[str, str] = {}
    for linha in texto[4:fim].splitlines():
        if ":" in linha and not linha.startswith(" "):
            chave, _, valor = linha.partition(":")
            campos[chave.strip()] = valor.strip().strip('"').strip("'")
    return campos


def checar_skill(pasta: Path) -> list[str]:
    erros: list[str] = []
    arquivo = pasta / "SKILL.md"
    if not arquivo.exists():
        return [f"{pasta.name}: sem SKILL.md"]
    texto = arquivo.read_text(encoding="utf-8")
    fm = frontmatter(texto)
    if fm is None:
        return [f"{pasta.name}: SKILL.md sem frontmatter YAML"]
    nome = fm.get("name", "")
    desc = fm.get("description", "")
    if not nome:
        erros.append(f"{pasta.name}: frontmatter sem `name`")
    elif nome != pasta.name:
        erros.append(f"{pasta.name}: `name: {nome}` difere da pasta")
    elif not RE_NOME.match(nome) or len(nome) > 64:
        erros.append(f"{pasta.name}: `name` inválido (a-z, 0-9, hífens simples, até 64)")
    if not desc:
        erros.append(f"{pasta.name}: frontmatter sem `description`")
    elif len(desc) > 1024:
        erros.append(f"{pasta.name}: `description` com {len(desc)} caracteres (máx. 1024)")
    for chave, valor in fm.items():
        if ": " in valor and not valor.startswith(('"', "'")):
            erros.append(
                f"{pasta.name}: `{chave}` tem ': ' sem aspas — YAML inválido, "
                "instaladores pulam a skill"
            )
    linhas = texto.count("\n") + 1
    if linhas > 500:
        erros.append(f"{pasta.name}: SKILL.md com {linhas} linhas (máx. 500)")

    for md in sorted(pasta.rglob("*.md")):
        conteudo = md.read_text(encoding="utf-8")
        rel = md.relative_to(SKILLS)
        for tool in RE_TOOL.findall(conteudo):
            if tool not in TOOLS_DO_MCP:
                erros.append(f"{rel}: tool `{tool}` não existe no MCP")
        for dominio in RE_LINK.findall(conteudo):
            if dominio not in DOMINIOS_PERMITIDOS:
                erros.append(f"{rel}: link para domínio não permitido: {dominio}")
        if md == arquivo:
            for ref in RE_REF.findall(conteudo):
                if not (pasta / ref).exists():
                    erros.append(f"{rel}: referência inexistente: {ref}")
    return erros


def main() -> int:
    pastas = sorted(p for p in SKILLS.iterdir() if p.is_dir() and not p.name.startswith("_"))
    if not pastas:
        print("nenhuma skill em skills/", flush=True)
        return 1
    erros: list[str] = []
    for pasta in pastas:
        e = checar_skill(pasta)
        print(f"{'ok ' if not e else 'ERRO'} {pasta.name}", flush=True)
        erros.extend(e)
    for e in erros:
        print(f"  - {e}", flush=True)
    print(f"{len(pastas)} skills, {len(erros)} erros", flush=True)
    return 1 if erros else 0


if __name__ == "__main__":
    sys.exit(main())
