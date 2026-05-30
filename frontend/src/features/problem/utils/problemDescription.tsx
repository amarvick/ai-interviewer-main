import type { Token, Tokens } from "marked";
import type { ReactNode } from "react";

export function isSafeHref(href: string) {
  return (
    href.startsWith("/") ||
    href.startsWith("#") ||
    href.startsWith("https://") ||
    href.startsWith("http://") ||
    href.startsWith("mailto:")
  );
}

export function childTokens(token: Token): Token[] {
  return "tokens" in token && Array.isArray(token.tokens) ? token.tokens : [];
}

export function decodeMarkdownText(text: string) {
  return text
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&amp;/g, "&")
    .replace(/&quot;/g, '"')
    .replace(/&#39;/g, "'");
}

export function renderInlineTokens(
  tokens: Token[],
  keyPrefix: string
): ReactNode[] {
  return tokens.map((token, index) => {
    const key = `${keyPrefix}-${index}`;

    switch (token.type) {
      case "text": {
        const textToken = token as Tokens.Text;
        return textToken.tokens
          ? renderInlineTokens(textToken.tokens, key)
          : decodeMarkdownText(textToken.text);
      }
      case "escape": {
        const escapeToken = token as Tokens.Escape;
        return decodeMarkdownText(escapeToken.text);
      }
      case "strong":
        return (
          <strong key={key}>
            {renderInlineTokens(childTokens(token), key)}
          </strong>
        );
      case "em":
        return <em key={key}>{renderInlineTokens(childTokens(token), key)}</em>;
      case "codespan": {
        const codeToken = token as Tokens.Codespan;
        return <code key={key}>{codeToken.text}</code>;
      }
      case "br":
        return <br key={key} />;
      case "del":
        return (
          <del key={key}>{renderInlineTokens(childTokens(token), key)}</del>
        );
      case "link": {
        const linkToken = token as Tokens.Link;
        if (!isSafeHref(linkToken.href)) {
          return decodeMarkdownText(linkToken.text);
        }
        return (
          <a
            key={key}
            href={linkToken.href}
            title={linkToken.title ?? undefined}
          >
            {renderInlineTokens(linkToken.tokens, key)}
          </a>
        );
      }
      case "image": {
        const imageToken = token as Tokens.Image;
        return decodeMarkdownText(imageToken.text);
      }
      case "html": {
        const htmlToken = token as Tokens.HTML;
        return decodeMarkdownText(htmlToken.raw);
      }
      default:
        return childTokens(token).length > 0
          ? renderInlineTokens(childTokens(token), key)
          : decodeMarkdownText(token.raw);
    }
  });
}

export function renderBlockToken(token: Token, index: number): ReactNode {
  const key = `block-${index}`;

  switch (token.type) {
    case "space":
    case "def":
      return null;
    case "heading": {
      const headingToken = token as Tokens.Heading;
      if (headingToken.depth <= 1) {
        return (
          <h3 key={key}>{renderInlineTokens(headingToken.tokens, key)}</h3>
        );
      }
      if (headingToken.depth === 2) {
        return (
          <h4 key={key}>{renderInlineTokens(headingToken.tokens, key)}</h4>
        );
      }
      return <h5 key={key}>{renderInlineTokens(headingToken.tokens, key)}</h5>;
    }
    case "paragraph": {
      const paragraphToken = token as Tokens.Paragraph;
      return <p key={key}>{renderInlineTokens(paragraphToken.tokens, key)}</p>;
    }
    case "text": {
      const textToken = token as Tokens.Text;
      return (
        <p key={key}>
          {textToken.tokens
            ? renderInlineTokens(textToken.tokens, key)
            : decodeMarkdownText(textToken.text)}
        </p>
      );
    }
    case "code": {
      const codeToken = token as Tokens.Code;
      return (
        <pre key={key}>
          <code>{codeToken.text}</code>
        </pre>
      );
    }
    case "list": {
      const listToken = token as Tokens.List;
      const ListTag = listToken.ordered ? "ol" : "ul";
      return (
        <ListTag
          key={key}
          start={
            listToken.ordered && listToken.start ? listToken.start : undefined
          }
        >
          {listToken.items.map((item, itemIndex) => (
            <li key={`${key}-item-${itemIndex}`}>
              {item.tokens.map((itemToken, tokenIndex) =>
                renderBlockToken(itemToken, tokenIndex)
              )}
            </li>
          ))}
        </ListTag>
      );
    }
    case "blockquote": {
      const blockquoteToken = token as Tokens.Blockquote;
      return (
        <blockquote key={key}>
          {blockquoteToken.tokens.map((childToken, childIndex) =>
            renderBlockToken(childToken, childIndex)
          )}
        </blockquote>
      );
    }
    case "hr":
      return <hr key={key} />;
    case "html": {
      const htmlToken = token as Tokens.HTML;
      return <p key={key}>{decodeMarkdownText(htmlToken.raw)}</p>;
    }
    default:
      return childTokens(token).length > 0 ? (
        <div key={key}>
          {childTokens(token).map((childToken, childIndex) =>
            renderBlockToken(childToken, childIndex)
          )}
        </div>
      ) : (
        <p key={key}>{decodeMarkdownText(token.raw)}</p>
      );
  }
}
